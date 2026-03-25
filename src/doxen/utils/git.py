"""Git history utilities."""

from datetime import datetime
from pathlib import Path
from typing import Any, Optional

import git


class GitAnalyzer:
    """Extract git history and metadata."""

    def __init__(self, repo_path: Path) -> None:
        """Initialize git analyzer.

        Args:
            repo_path: Path to git repository
        """
        try:
            self.repo = git.Repo(repo_path, search_parent_directories=True)
        except git.InvalidGitRepositoryError:
            self.repo = None

    def get_file_history(self, file_path: Path) -> dict[str, Any]:
        """Get git history for a specific file.

        Args:
            file_path: Path to file

        Returns:
            Dictionary with git metadata
        """
        if not self.repo:
            return {}

        try:
            commits = list(self.repo.iter_commits(paths=str(file_path), max_count=10))
            if not commits:
                return {}

            latest_commit = commits[0]
            return {
                "commit_hash": latest_commit.hexsha[:8],
                "author": latest_commit.author.name,
                "email": latest_commit.author.email,
                "last_modified": datetime.fromtimestamp(latest_commit.committed_date).isoformat(),
                "message": latest_commit.message.strip(),
                "recent_commits": [
                    {
                        "hash": c.hexsha[:8],
                        "message": c.message.strip().split("\n")[0],
                        "date": datetime.fromtimestamp(c.committed_date).isoformat(),
                    }
                    for c in commits[:5]
                ],
            }
        except Exception:
            return {}
