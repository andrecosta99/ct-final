from unittest.mock import Mock, patch

import pytest

from committracker.plugins.git_statistics import (categorize_commit_type,
                                                  extract_branches_info)


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


@pytest.mark.parametrize(
    "repo_path, expected_branches_info",
    [
        # Caminho fictício e informações esperadas de branches
        ("caminho/para/repositorio/ficticio", {"main": 10, "develop": 5}),
    ],
)
def test_extract_branches_info(repo_path, expected_branches_info, mocker):
    # Cria mocks para as branches com os nomes 'main' e 'develop'
    main_branch_mock = Mock()
    develop_branch_mock = Mock()
    mocker.patch.object(main_branch_mock, "name", "main")
    mocker.patch.object(develop_branch_mock, "name", "develop")

    # Configura o mock_repo para usar os mocks de branch criados
    mock_repo = Mock()
    mock_repo.branches = [main_branch_mock, develop_branch_mock]
    mock_repo.iter_commits.side_effect = [
        range(10),
        range(5),
    ]  # 10 commits em "main", 5 em "develop"

    with patch("committracker.plugins.git_statistics.Repo", return_value=mock_repo):
        branches_info = extract_branches_info(repo_path)
        # Constrói o dicionário de branches_info esperado usando os nomes das branches como chaves
        expected_branches_info_mocked = {
            branch_mock.name: count
            for branch_mock, count in zip(mock_repo.branches, [10, 5])
        }
        assert branches_info == expected_branches_info_mocked
