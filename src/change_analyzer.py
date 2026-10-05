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


def filter_source_files(files):
    ignored_files = [
        "data/",
        "results/",
        "__pycache__/",
        ".pyc"
    ]

    filtered = []

    for file in files:
        file = file.strip().replace("\\", "/")

        if any(
            ignored in file
            for ignored in ignored_files
        ):
            continue

        if file.startswith("app/") and file.endswith(".py"):
            filtered.append(file)

    return sorted(set(filtered))


def get_changed_files():

    # Used by CI/CD when changed files are explicitly provided.
    ci_changed_files = os.getenv("CHANGED_FILES")

    if ci_changed_files:
        return filter_source_files(
            ci_changed_files.split(",")
        )

    # First check local unstaged changes.
    changed = run_git_command(
        [
            "git",
            "diff",
            "--name-only"
        ]
    )

    changed = filter_source_files(changed)

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

    changed = filter_source_files(changed)

    if changed:
        return changed

    # In CI/CD, compare the current commit with previous commit.
    changed = run_git_command(
        [
            "git",
            "diff",
            "--name-only",
            "HEAD^",
            "HEAD"
        ]
    )

    return filter_source_files(changed)