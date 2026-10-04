import os
import subprocess


def run_git_command(command):
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False
        )

        if result.returncode == 0:
            return [
                line.strip().replace("\\", "/")
                for line in result.stdout.splitlines()
                if line.strip()
            ]

    except Exception:
        pass

    return []


def get_changed_files():

    # Used by CI/CD when the changed files
    # are explicitly provided.
    ci_changed_files = os.getenv(
        "CHANGED_FILES"
    )

    if ci_changed_files:

        return sorted(
            set(
                file.strip().replace("\\", "/")
                for file in ci_changed_files.split(",")
                if file.strip()
            )
        )

    # Compare current commit with previous commit.
    changed = run_git_command(
        [
            "git",
            "diff",
            "--name-only",
            "HEAD^",
            "HEAD"
        ]
    )

    if changed:
        return changed

    # Check local unstaged changes.
    changed = run_git_command(
        [
            "git",
            "diff",
            "--name-only"
        ]
    )

    if changed:
        return changed

    # Check staged changes.
    changed = run_git_command(
        [
            "git",
            "diff",
            "--cached",
            "--name-only"
        ]
    )

    return changed