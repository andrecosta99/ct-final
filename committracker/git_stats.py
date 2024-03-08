import logging
import shutil
import tempfile
from collections import Counter

from git import Repo

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def clone_remote_repo(url):
    temp_dir = tempfile.mkdtemp()
    try:
        Repo.clone_from(url, temp_dir)
        logging.info(f"Successfully cloned repository to {temp_dir}")
        return temp_dir
    except Exception as e:
        logging.error(f"Error cloning repository: {e}")
        try:
            shutil.rmtree(temp_dir)
            logging.info(f"Temporary directory {temp_dir} successfully removed")
        except Exception as e_rm:
            logging.error(f"Error removing temporary directory: {e_rm}")
        return None


def categorize_commit_type(commit_message):
    lower_msg = commit_message.lower()
    if "fix" in lower_msg or "bug" in lower_msg:
        return "Bug Fix"
    elif "feature" in lower_msg or "add" in lower_msg:
        return "Feature"
    elif "doc" in lower_msg or "readme" in lower_msg:
        return "Documentation"
    else:
        return "Other"


def extract_git_stats(repo_path):
    try:
        repo = Repo(repo_path)
        commits = list(repo.iter_commits())

        contributors = Counter(commit.author.name for commit in commits)
        commit_dates = [commit.committed_datetime for commit in commits]
        commit_types = Counter(
            categorize_commit_type(commit.message) for commit in commits
        )

        total_lines_added = 0
        total_lines_deleted = 0
        for commit in commits:
            stats = commit.stats.total
            total_lines_added += stats["insertions"]
            total_lines_deleted += stats["deletions"]

        average_lines_per_commit = (
            (total_lines_added + total_lines_deleted) / len(commits) if commits else 0
        )

        return {
            "total_commits": len(commits),
            "contributors": contributors,
            "commit_dates": commit_dates,
            "commit_types": commit_types,
            "average_lines_per_commit": average_lines_per_commit,
        }
    except Exception as e:
        logging.error(f"Error extracting git statistics: {e}")
        return {"error": "Failed to extract repository statistics."}


def extract_branches_info_new(repo_path):
    try:
        repo = Repo(repo_path)
        branches_info = {}
        for branch in repo.branches:
            commits_count = sum(1 for _ in repo.iter_commits(branch))
            branches_info[branch.name] = commits_count
        return branches_info
    except Exception as e:
        logging.error(f"Error extracting branches information: {e}")
        return {"error": "Failed to extract branches information."}
