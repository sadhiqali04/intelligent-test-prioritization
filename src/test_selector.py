import json
from pathlib import Path


BASE_DIR = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)

MAPPING_FILE = (
    BASE_DIR
    / "data"
    / "test_mapping.json"
)


def load_mapping():

    return json.loads(
        MAPPING_FILE.read_text(
            encoding="utf-8"
        )
    )


def select_tests(changed_files):

    mapping = load_mapping()

    changed_files = {
        file.replace("\\", "/")
        for file in changed_files
    }

    selected = []

    for test, source_files in mapping.items():

        if changed_files.intersection(
            source_files
        ):
            selected.append(test)

    return sorted(selected)