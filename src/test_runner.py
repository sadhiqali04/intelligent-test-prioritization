import json
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path


BASE_DIR = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)

HISTORY_FILE = (
    BASE_DIR
    / "data"
    / "test_history.json"
)

RESULTS_FILE = (
    BASE_DIR
    / "results"
    / "results.json"
)


def load_history():

    return json.loads(
        HISTORY_FILE.read_text(
            encoding="utf-8"
        )
    )


def save_history(history):

    HISTORY_FILE.write_text(
        json.dumps(
            history,
            indent=2
        ),
        encoding="utf-8"
    )


def run_tests(test_paths):

    history = load_history()

    results_directory = (
        BASE_DIR
        / "results"
    )

    results_directory.mkdir(
        exist_ok=True
    )

    junit_file = (
        results_directory
        / "prioritized_tests.xml"
    )

    if junit_file.exists():
        junit_file.unlink()

    start = time.perf_counter()

    command = [
        sys.executable,
        "-m",
        "pytest",
        *test_paths,
        "-q",
        f"--junitxml={junit_file}"
    ]

    process = subprocess.run(
        command,
        cwd=BASE_DIR,
        capture_output=True,
        text=True
    )

    wall_time = (
        time.perf_counter()
        - start
    )

    results = []

    if junit_file.exists():

        root = ET.parse(
            junit_file
        ).getroot()

        testcases = root.findall(
            ".//testcase"
        )

        for test_path in test_paths:

            test_name = Path(
                test_path
            ).stem

            matching_cases = [
                case
                for case in testcases
                if test_name in case.attrib.get(
                    "classname",
                    ""
                )
            ]

            execution_time = sum(
                float(
                    case.attrib.get(
                        "time",
                        "0"
                    )
                )
                for case in matching_cases
            )

            failed = any(
                case.find("failure")
                is not None
                or case.find("error")
                is not None
                for case in matching_cases
            )

            status = (
                "FAILED"
                if failed
                else "PASSED"
            )

            record = history.setdefault(
                test_path,
                {
                    "total_runs": 0,
                    "failures": 0,
                    "average_execution_time": 0.0,
                    "last_result": "not_run"
                }
            )

            old_runs = record[
                "total_runs"
            ]

            record[
                "total_runs"
            ] = old_runs + 1

            if failed:

                record[
                    "failures"
                ] += 1

            record[
                "average_execution_time"
            ] = round(
                (
                    (
                        record[
                            "average_execution_time"
                        ]
                        * old_runs
                    )
                    + execution_time
                )
                / record[
                    "total_runs"
                ],
                4
            )

            record[
                "last_result"
            ] = status.lower()

            results.append(
                {
                    "test": test_path,
                    "status": status,
                    "execution_time": round(
                        execution_time,
                        4
                    )
                }
            )

    # If JUnit parsing did not produce results,
    # still return a useful pipeline result.
    if not results:

        status = (
            "FAILED"
            if process.returncode != 0
            else "PASSED"
        )

        for test_path in test_paths:

            results.append(
                {
                    "test": test_path,
                    "status": status,
                    "execution_time": round(
                        wall_time,
                        4
                    )
                }
            )

    save_history(history)

    RESULTS_FILE.write_text(
        json.dumps(
            {
                "results": results,
                "wall_clock_time": round(
                    wall_time,
                    4
                ),
                "pytest_return_code":
                    process.returncode
            },
            indent=2
        ),
        encoding="utf-8"
    )

    selected_test_time = sum(
        item["execution_time"]
        for item in results
    )

    return (
        results,
        selected_test_time
    )