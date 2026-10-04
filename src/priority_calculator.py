import json
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

MAPPING_FILE = (
    BASE_DIR
    / "data"
    / "test_mapping.json"
)


def load_history():

    return json.loads(
        HISTORY_FILE.read_text(
            encoding="utf-8"
        )
    )


def calculate_priority(
    selected_tests,
    changed_files
):

    history = load_history()

    mapping = json.loads(
        MAPPING_FILE.read_text(
            encoding="utf-8"
        )
    )

    times = [
        float(
            history.get(
                test,
                {}
            ).get(
                "average_execution_time",
                0.0
            )
        )
        for test in selected_tests
    ]

    min_time = min(times) if times else 0.0
    max_time = max(times) if times else 0.0

    changed_files = {
        file.replace("\\", "/")
        for file in changed_files
    }

    results = []

    for test in selected_tests:

        record = history.get(
            test,
            {}
        )

        total_runs = int(
            record.get(
                "total_runs",
                0
            )
        )

        failures = int(
            record.get(
                "failures",
                0
            )
        )

        # --------------------------------
        # FACTOR 1
        # Code-change relevance
        # --------------------------------

        relevance = 1.0 if (
            changed_files.intersection(
                mapping.get(
                    test,
                    []
                )
            )
        ) else 0.0

        # --------------------------------
        # FACTOR 2
        # Historical failure probability
        # --------------------------------

        if total_runs > 0:

            failure_probability = (
                failures / total_runs
            )

        else:

            failure_probability = 0.0

        # --------------------------------
        # FACTOR 3
        # Execution efficiency
        # --------------------------------

        execution_time = float(
            record.get(
                "average_execution_time",
                0.0
            )
        )

        if max_time == min_time:

            execution_efficiency = 1.0

        else:

            normalized_time = (
                execution_time - min_time
            ) / (
                max_time - min_time
            )

            execution_efficiency = (
                1.0 - normalized_time
            )

        # --------------------------------
        # DCATP FORMULA
        # --------------------------------

        priority_score = (
            0.5 * relevance
            + 0.3 * failure_probability
            + 0.2 * execution_efficiency
        )

        results.append(
            {
                "test": test,
                "code_relevance": round(
                    relevance,
                    4
                ),
                "failure_probability": round(
                    failure_probability,
                    4
                ),
                "execution_efficiency": round(
                    execution_efficiency,
                    4
                ),
                "priority_score": round(
                    priority_score,
                    4
                )
            }
        )

    return sorted(
        results,
        key=lambda item:
            item["priority_score"],
        reverse=True
    )