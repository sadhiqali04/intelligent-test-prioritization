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


def evaluate(
    selected_count,
    selected_duration,
    total_count
):

    results_directory = (
        BASE_DIR
        / "results"
    )

    results_directory.mkdir(
        exist_ok=True
    )

    junit_file = (
        results_directory
        / "full_suite.xml"
    )

    if junit_file.exists():
        junit_file.unlink()

    start = time.perf_counter()

    process = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "tests",
            "-q",
            f"--junitxml={junit_file}"
        ],
        cwd=BASE_DIR,
        capture_output=True,
        text=True
    )

    wall_time = (
        time.perf_counter()
        - start
    )

    full_test_time = 0.0
    full_failed_tests = 0
    full_passed_tests = 0

    if junit_file.exists():

        root = ET.parse(
            junit_file
        ).getroot()

        testcases = root.findall(
            ".//testcase"
        )

        for case in testcases:

            full_test_time += float(
                case.attrib.get(
                    "time",
                    "0"
                )
            )

            if (
                case.find("failure")
                is not None
                or case.find("error")
                is not None
            ):

                full_failed_tests += 1

            else:

                full_passed_tests += 1

    test_reduction = 0.0

    if total_count > 0:

        test_reduction = (
            (
                total_count
                - selected_count
            )
            / total_count
        ) * 100

    time_saving = 0.0

    if full_test_time > 0:

        time_saving = (
            (
                full_test_time
                - selected_duration
            )
            / full_test_time
        ) * 100

    return {
        "full_suite_passed":
            process.returncode == 0,

        "full_suite_test_count":
            total_count,

        "selected_test_count":
            selected_count,

        "full_suite_failed_tests":
            full_failed_tests,

        "full_suite_passed_tests":
            full_passed_tests,

        "test_reduction_percent":
            round(
                test_reduction,
                2
            ),

        "full_suite_test_execution_time":
            round(
                full_test_time,
                4
            ),

        "selected_suite_test_execution_time":
            round(
                selected_duration,
                4
            ),

        "test_execution_time_saving_percent":
            round(
                time_saving,
                2
            ),

        "full_suite_wall_clock_time":
            round(
                wall_time,
                4
            ),

        "resource_usage_proxy_reduction_percent":
            round(
                test_reduction,
                2
            )
    }