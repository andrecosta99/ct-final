import pytest

from committracker.git_stats import categorize_commit_type


@pytest.mark.parametrize(
    "commit_message, expected_category",
    [
        ("fixed a bug in the login feature", "Bug Fix"),
        ("add a new feature for user profiles", "Feature"),
        ("updated the README with new instructions", "Documentation"),
        ("refactored the entire codebase for clarity", "Other"),
    ],
)
def test_categorize_commit_type(commit_message, expected_category):
    assert categorize_commit_type(commit_message) == expected_category
