#!/usr/bin/env python3

import subprocess
from pathlib import Path
import requests
import os

VERSION_FILE = Path("VERSION")

# -------------------------
# Version helpers
# -------------------------
def read_version():
    return VERSION_FILE.read_text().strip() if VERSION_FILE.exists() else "0.0.0"

def write_version(version):
    VERSION_FILE.write_text(version + "\n")

def bump_version(current, part):
    major, minor, patch = map(int, current.split("."))
    if part == "major":
        major += 1
        minor = 0
        patch = 0
    elif part == "minor":
        minor += 1
        patch = 0
    elif part == "patch":
        patch += 1
    return f"{major}.{minor}.{patch}"

# -------------------------
# Shell helpers
# -------------------------
def run(cmd):
    print(f">>> {cmd}")
    subprocess.run(cmd, shell=True, check=True)

# -------------------------
# Semantic analysis
# -------------------------
def determine_bump():
    result = subprocess.run(
        "git describe --tags --abbrev=0",
        shell=True,
        capture_output=True,
        text=True,
    )

    last_tag = result.stdout.strip() if result.returncode == 0 else ""
    commits_cmd = (
        f"git log {last_tag}..HEAD --pretty=%s"
        if last_tag
        else "git log HEAD --pretty=%s"
    )

    commits = (
        subprocess.run(commits_cmd, shell=True, capture_output=True, text=True)
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

# -------------------------
# Deploy integrations
# -------------------------
def update_render_env(app_version, hook_url):
    if not hook_url:
        print("⚠️ Render deploy hook not set. Skipping Render deployment.")
        return

    print(f"Triggering Render deployment with APP_VERSION={app_version}")
    payload = {"APP_VERSION": app_version}

    response = requests.post(hook_url, json=payload, timeout=10)
    if response.ok:
        print("Render deployment triggered successfully.")
    else:
        print(f"Render deploy failed: {response.status_code}, {response.text}")

def update_netlify_env(app_version, site_id, auth_token):
    if not site_id or not auth_token:
        print("⚠️ Netlify credentials not set. Skipping Netlify update.")
        return

    print(f"Updating Netlify environment APP_VERSION={app_version}")
    url = f"https://api.netlify.com/api/v1/sites/{site_id}/env"
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json",
    }

    payload = {"key": "APP_VERSION", "value": app_version}
    response = requests.post(url, json=payload, headers=headers, timeout=10)

    if response.ok:
        print("Netlify APP_VERSION updated successfully.")
    else:
        print(f"Netlify update failed: {response.status_code}, {response.text}")

# -------------------------
# Main
# -------------------------
def main():
    print("=== Semantic Release Automation ===")

    # 🔒 Idempotency guard
    if subprocess.run(
        "git tag --points-at HEAD",
        shell=True,
        capture_output=True,
        text=True,
    ).stdout.strip():
        print("HEAD already tagged. Skipping release.")
        return

    bump_type = determine_bump()
    current_version = read_version()
    new_version = bump_version(current_version, bump_type)

    print(f"Version bump: {current_version} -> {new_version} ({bump_type})")
    write_version(new_version)

    # Optional backend migration
    backend_changes = subprocess.run(
        "git diff --name-only HEAD~1 HEAD backend/",
        shell=True,
        capture_output=True,
        text=True,
    ).stdout.strip()

    if backend_changes:
        print("Backend changed, creating Alembic migration...")
        run(f"cd backend && flask db migrate -m 'Auto migration for v{new_version}'")
        run("cd backend && flask db upgrade")
        run("git add backend/migrations")

    # Commit + tag
    run("git add VERSION")
    run(f"git commit -m 'chore(release): v{new_version}'")
    run(f"git tag v{new_version}")
    run("git push origin HEAD")
    run("git push origin --tags")

    # Deploy
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

    print(f"Release v{new_version} complete.")

if __name__ == "__main__":
    main()
