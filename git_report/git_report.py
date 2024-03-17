import json
import subprocess
from typing import Any

NUM_CHARS = [str(n) for n in range(10)]


def run_command(command: str) -> Any:
    return subprocess.check_output(command, shell=True).decode("utf-8")


def get_latest_tag() -> Any:
    command: str = "git describe --tags --abbrev=0"
    return run_command(command)


def get_latest_tag_timestamp() -> Any:
    latest_tag = get_latest_tag()
    command: str = f"git log -1 --format=%aI {latest_tag}"
    return run_command(command)


def get_n_days_ago_timestamp(n: str) -> Any:
    command: str = f'date -d "{n} days ago" + "%F"'
    return run_command(command)


def get_git_stats(since: str) -> Any:
    command: str = f"git-stats --raw --authors --since {since}"
    return json.loads(run_command(command))


def get_total_commits(git_stats: Any) -> int:
    return sum(author["value"] for author in git_stats["authors"])


def get_author_info(author: dict[str, str], since: str) -> str:
    author_name: str = author["label"]
    command: str = (
        f'git log --author="{author_name}" --numstat --since="{since}" --format=""'
    )
    log: str = run_command(command)
    files_changed: int = 0
    lines_added: int = 0
    lines_deleted: int = 0
    for line in log.splitlines():
        if not line:
            continue
        added, deleted, _ = line.split("\t", 2)
        files_changed += 1
        if added[-1] in NUM_CHARS:
            lines_added += int(added)
        if added[-1] in NUM_CHARS:
            lines_deleted += int(deleted)
    return f"\n* {files_changed} Files Changed, {lines_added} (+) Lines Added, {lines_deleted} (-) Lines Deleted"  # pylint: disable=line-too-long


def run(s: str = "-1") -> None:
    timestamp: str = get_n_days_ago_timestamp(s)
    if s == "-1":  # pylint: disable=magic-value-comparison
        timestamp = get_latest_tag_timestamp()
    git_stats: Any = get_git_stats(timestamp)
    total_commits: int = get_total_commits(git_stats)

    for author in git_stats["authors"]:
        author_info: str = get_author_info(author, timestamp)
        percentage_of_total: float = (author["value"] * 100) / total_commits
        print(
            f'{author["label"]}: {author["value"]} commits ({percentage_of_total:.2f}% of total) {author_info}\n'  # pylint: disable=line-too-long
        )
