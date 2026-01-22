#!/usr/bin/env python3

import subprocess
from pathlib import Path
import requests
import os
import sys
from datetime import datetime

VERSION_FILE = Path("VERSION")

# -------------------------------------------------
# Semantic version helpers
# -------------------------------------------------
def read_version():
    return VERSION_FILE.read_text().strip() if VERSION_FILE.exists() else "0.0.0"


def write_version(version: str):
    VERSION_FILE.write_text(version + "\n")


def bump_version(current: str, part: str) -> str:
    major, minor, patch = map(int, current.split("."))

    if part == "major":
        major += 1
        minor = 0
        patch = 0
    elif part == "minor":
        minor += 1
        patch = 0
    else:
        patch += 1

    return f"{major}.{minor}.{patch}"


# -------------------------------------------------
# Calendar version helpers
# -------------------------------------------------
WEEK_LETTERS = "ABCDE"
DAY_LETTERS = "ABCDEFG"  # Mon → Sun


def calendar_version(env: str) -> str:
    now = datetime.utcnow()

    year = now.year
    month = f"{now.month:02d}"

    week_of_month = (now.day - 1) // 7
    week_letter = WEEK_LETTERS[week_of_month]

    day_letter = DAY_LETTERS[now.weekday()]

    prefix = f"{year}.{month}.{week_letter}{day_letter}"

    # count existing tags today
    tag_prefix = f"+{prefix}"
    tags = subprocess.getoutput("git tag").splitlines()
    daily_count = (
        sum(1 for t in tags if tag_prefix in t) + 1
    )

    return f"{prefix}{daily_count}_{env}"


# -------------------------------------------------
# Shell helpers
# -------------------------------------------------
def run(cmd: str):
    print(f">>> {cmd}")
    subprocess.run(cmd, shell=True, check=True)


def tag_exists(tag: str) -> bool:
    return (
        subprocess.run(
            f"git rev-parse -q --verify refs/tags/{tag}",
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        ).returncode
        == 0
    )


# -------------------------------------------------
# Semantic analysis
# -------------------------------------------------
def determine_bump() -> str:
    last_tag_cmd = subprocess.run(
        "git describe --tags --abbrev=0",
        shell=True,
        capture_output=True,
        text=True,
    )

    last_tag = last_tag_cmd.stdout.strip() if last_tag_cmd.returncode == 0 else ""

    log_cmd = (
        f"git log {last_tag}..HEAD --pretty=%s"
        if last_tag
        else "git log HEAD --pretty=%s"
    )

    commits = subprocess.getoutput(log_cmd).splitlines()

    bump = "patch"
    for c in commits:
        if "BREAKING CHANGE" in c:
            return "major"
        if c.startswith("feat:"):
            bump = "minor"

    return bump


# -------------------------------------------------
# Deploy integrations
# -------------------------------------------------
def update_render_env(version: str, hook_url: str | None):
    if not hook_url:
        print("⚠️ Render deploy hook not set. Skipping Render.")
        return

    print(f"Triggering Render deployment with APP_VERSION={version}")
    requests.post(hook_url, json={"APP_VERSION": version}, timeout=10)


def update_netlify_env(version: str, site_id: str | None, token: str | None):
    if not site_id or not token:
        print("⚠️ Netlify credentials not set. Skipping Netlify.")
        return

    url = f"https://api.netlify.com/api/v1/sites/{site_id}/env"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    requests.post(
        url,
        headers=headers,
        json={"key": "APP_VERSION", "value": version},
        timeout=10,
    )


# -------------------------------------------------
# Main
# -------------------------------------------------
def main():
    print("=== Dual Version Release Automation ===")

    if os.getenv("GITHUB_EVENT_NAME") == "pull_request":
        print("Pull request detected. Skipping release.")
        sys.exit(0)

    if subprocess.getoutput("git tag --points-at HEAD"):
        print("HEAD already tagged. Skipping release.")
        sys.exit(0)

    bump_type = determine_bump()
    current_version = read_version()
    new_semver = bump_version(current_version, bump_type)

    branch = os.getenv("GITHUB_REF_NAME") or subprocess.getoutput(
        "git rev-parse --abbrev-ref HEAD"
    )

    env = "DEV" if branch == "develop" else "PROD"
    calver = calendar_version(env)

    full_tag = f"v{new_semver}+{calver}"

    if tag_exists(full_tag):
        print(f"Tag {full_tag} already exists. Aborting.")
        sys.exit(0)

    print(f"SemVer:   {current_version} → {new_semver}")
    print(f"CalVer:   {calver}")

    write_version(new_semver)

    run("git add VERSION")
    run(f"git commit -m 'chore(release): v{new_semver}'")
    run(f"git tag {full_tag}")
    run("git push origin HEAD")
    run("git push origin --tags")

    if branch == "develop":
        update_render_env(calver, os.getenv("RENDER_STAGING_DEPLOY_HOOK"))
        update_netlify_env(
            calver,
            os.getenv("NETLIFY_STAGING_SITE_ID"),
            os.getenv("NETLIFY_AUTH_TOKEN"),
        )

    elif branch == "main":
        update_render_env(calver, os.getenv("RENDER_PROD_DEPLOY_HOOK"))
        update_netlify_env(
            calver,
            os.getenv("NETLIFY_PROD_SITE_ID"),
            os.getenv("NETLIFY_AUTH_TOKEN"),
        )

    print(f"✅ Release {full_tag} completed successfully.")


if __name__ == "__main__":
    main()

