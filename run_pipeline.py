import json
from pathlib import Path

from src.change_analyzer import (
    get_changed_files
)

from src.evaluation import (
    evaluate
)

from src.priority_calculator import (
    calculate_priority
)

from src.test_runner import (
    run_tests
)

from src.test_selector import (
    load_mapping,
    select_tests
)


BASE_DIR = Path(__file__).resolve().parent


def main():

    print()
    print("=" * 60)
    print(
        "INTELLIGENT TEST SELECTION "
        "AND PRIORITIZATION"
    )
    print("=" * 60)

    # -----------------------------------------
    # STEP 1: Load complete test mapping
    # -----------------------------------------

    mapping = load_mapping()

    all_tests = sorted(
        mapping.keys()
    )

    # -----------------------------------------
    # STEP 2: Detect changed files
    # -----------------------------------------

    changed_files = (
        get_changed_files()
    )

    print()
    print("1. CHANGE ANALYSIS")
    print("-" * 60)

    if changed_files:

        for file in changed_files:
            print(
                f"Changed file: {file}"
            )

    else:

        print(
            "No code changes detected."
        )

    # -----------------------------------------
    # STEP 3: Select relevant tests
    # -----------------------------------------

    selected_tests = select_tests(
        changed_files
    )

    # Initial baseline:
    # If there are no detectable changes,
    # run all tests.
    if not selected_tests:

        print()
        print(
            "No specific tests selected."
        )

        print(
            "Running complete test suite "
            "for baseline."
        )

        selected_tests = all_tests

    print()
    print("2. TEST SELECTION")
    print("-" * 60)

    for test in selected_tests:
        print(
            f"Selected: {test}"
        )

    # -----------------------------------------
    # STEP 4: DCATP prioritization
    # -----------------------------------------

    ranking = calculate_priority(
        selected_tests,
        changed_files
    )

    print()
    print("3. DCATP PRIORITIZATION")
    print("-" * 60)

    print(
        "Formula:"
    )

    print(
        "Score = "
        "0.5(Relevance) + "
        "0.3(Failure Probability) + "
        "0.2(Execution Efficiency)"
    )

    print()

    for position, item in enumerate(
        ranking,
        start=1
    ):

        print(
            f"{position}. {item['test']}"
        )

        print(
            f"   Code Relevance: "
            f"{item['code_relevance']}"
        )

        print(
            f"   Failure Probability: "
            f"{item['failure_probability']}"
        )

        print(
            f"   Execution Efficiency: "
            f"{item['execution_efficiency']}"
        )

        print(
            f"   Priority Score: "
            f"{item['priority_score']}"
        )

    ordered_tests = [
        item["test"]
        for item in ranking
    ]

    # -----------------------------------------
    # STEP 5: Execute prioritized tests
    # -----------------------------------------

    print()
    print("4. PRIORITIZED TEST EXECUTION")
    print("-" * 60)

    (
        test_results,
        selected_execution_time
    ) = run_tests(
        ordered_tests
    )

    for result in test_results:

        print(
            f"{result['test']} -> "
            f"{result['status']} | "
            f"{result['execution_time']} seconds"
        )

    # -----------------------------------------
    # STEP 6: Full-suite evaluation
    # -----------------------------------------

    print()
    print("5. FULL SUITE EVALUATION")
    print("-" * 60)

    evaluation = evaluate(
        selected_count=len(
            ordered_tests
        ),
        selected_duration=(
            selected_execution_time
        ),
        total_count=len(
            all_tests
        )
    )

    print(
        f"Full Suite Tests: "
        f"{evaluation['full_suite_test_count']}"
    )

    print(
        f"Selected Tests: "
        f"{evaluation['selected_test_count']}"
    )

    print(
        f"Test Reduction: "
        f"{evaluation['test_reduction_percent']}%"
    )

    print(
        f"Full Suite Execution Time: "
        f"{evaluation['full_suite_test_execution_time']} seconds"
    )

    print(
        f"Selected Suite Execution Time: "
        f"{evaluation['selected_suite_test_execution_time']} seconds"
    )

    print(
        f"Execution Time Saving: "
        f"{evaluation['test_execution_time_saving_percent']}%"
    )

    print(
        f"Full Suite Passed: "
        f"{evaluation['full_suite_passed']}"
    )

    # -----------------------------------------
    # STEP 7: Save complete report
    # -----------------------------------------

    report = {
        "project": (
            "Intelligent Test Selection "
            "and Prioritization"
        ),

        "method": "DCATP",

        "formula": (
            "0.5*Code Relevance + "
            "0.3*Failure Probability + "
            "0.2*Execution Efficiency"
        ),

        "changed_files": changed_files,

        "all_tests": all_tests,

        "selected_tests": selected_tests,

        "dcatp_ranking": ranking,

        "test_results": test_results,

        "evaluation": evaluation
    }

    results_directory = (
        BASE_DIR
        / "results"
    )

    results_directory.mkdir(
        exist_ok=True
    )

    report_file = (
        results_directory
        / "pipeline_report.json"
    )

    report_file.write_text(
        json.dumps(
            report,
            indent=2
        ),
        encoding="utf-8"
    )

    print()
    print("=" * 60)
    print("PIPELINE COMPLETED")
    print("=" * 60)

    print(
        "Report:"
    )

    print(
        "results/pipeline_report.json"
    )


if __name__ == "__main__":
    main()