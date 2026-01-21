#!/usr/bin/env python3

import subprocess
from pathlib import Path
import requests
import os
import sys

VERSION_FILE = Path("VERSION")

# -------------------------------------------------
# Version helpers
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
    else:  # patch
        patch += 1

    return f"{major}.{minor}.{patch}"


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

    commits = (
        subprocess.run(log_cmd, shell=True, capture_output=True, text=True)
        .stdout.strip()
        .splitlines()
    )

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
    r = requests.post(hook_url, json={"APP_VERSION": version}, timeout=10)

    if r.ok:
        print("Render deployment triggered.")
    else:
        print(f"Render deploy failed: {r.status_code} {r.text}")


def update_netlify_env(version: str, site_id: str | None, token: str | None):
    if not site_id or not token:
        print("⚠️ Netlify credentials not set. Skipping Netlify.")
        return

    print(f"Updating Netlify APP_VERSION={version}")
    url = f"https://api.netlify.com/api/v1/sites/{site_id}/env"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    r = requests.post(
        url,
        headers=headers,
        json={"key": "APP_VERSION", "value": version},
        timeout=10,
    )

    if r.ok:
        print("Netlify APP_VERSION updated.")
    else:
        print(f"Netlify update failed: {r.status_code} {r.text}")


# -------------------------------------------------
# Main
# -------------------------------------------------
def main():
    print("=== Semantic Release Automation ===")

    # 🚫 Never release on PRs
    if os.getenv("GITHUB_EVENT_NAME") == "pull_request":
        print("Pull request detected. Skipping release.")
        sys.exit(0)

    # 🔒 Guard 1: HEAD already tagged
    existing = subprocess.run(
        "git tag --points-at HEAD",
        shell=True,
        capture_output=True,
        text=True,
    ).stdout.strip()

    if existing:
        print(f"HEAD already tagged ({existing}). Skipping release.")
        sys.exit(0)

    bump_type = determine_bump()
    current_version = read_version()
    new_version = bump_version(current_version, bump_type)
    new_tag = f"v{new_version}"

    # 🔒 Guard 2: tag exists anywhere
    if tag_exists(new_tag):
        print(f"Tag {new_tag} already exists. Aborting release.")
        sys.exit(0)

    print(f"Version bump: {current_version} → {new_version} ({bump_type})")

    write_version(new_version)

    run("git add VERSION")
    run(f"git commit -m 'chore(release): {new_tag}'")
    run(f"git tag {new_tag}")
    run("git push origin HEAD")
    run("git push origin --tags")

    branch = os.getenv("GITHUB_REF_NAME") or subprocess.getoutput(
        "git rev-parse --abbrev-ref HEAD"
    )

    if branch == "develop":
        update_render_env(new_version, os.getenv("RENDER_STAGING_DEPLOY_HOOK"))
        update_netlify_env(
            new_version,
            os.getenv("NETLIFY_STAGING_SITE_ID"),
            os.getenv("NETLIFY_AUTH_TOKEN"),
        )

    elif branch == "main":
        update_render_env(new_version, os.getenv("RENDER_PROD_DEPLOY_HOOK"))
        update_netlify_env(
            new_version,
            os.getenv("NETLIFY_PROD_SITE_ID"),
            os.getenv("NETLIFY_AUTH_TOKEN"),
        )

    print(f"✅ Release {new_tag} completed successfully.")


if __name__ == "__main__":
    main()
