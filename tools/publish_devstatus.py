"""Publish devstatus.json to the `devstatus` branch, from whichever branch updated it.

The website reads the roadmap from
https://raw.githubusercontent.com/SuIT-pub/Mind-the-School/devstatus/devstatus.json
so work on any branch shows up without waiting for a merge to master.

Several branches can carry their own devstatus.json. The newest `updatedAt`
wins; a push from an older branch never overwrites a newer published state.

Usage (GitHub Actions, see .github/workflows/publish-devstatus.yml):
    python tools/publish_devstatus.py devstatus.json <source-branch>

The commit is built with git plumbing straight from the file, so nothing is
checked out and the job's working tree is never touched.
"""

import json
import pathlib
import subprocess
import sys
from datetime import datetime

from validate_devstatus import validate

TARGET_BRANCH = "devstatus"
FILE_NAME = "devstatus.json"


def _instant(document):
    return datetime.fromisoformat(str(document["updatedAt"]).replace("Z", "+00:00"))


def should_publish(new, current):
    """True if `new` is strictly newer than the published `current` (or nothing usable is published)."""
    if current is None:
        return True
    try:
        return _instant(new) > _instant(current)
    except (KeyError, ValueError, TypeError):
        return True  # a broken published copy is always replaced


def _git(repo, *args, input_text=None, check=True):
    # Bytes in, bytes out: text mode would turn "\n" into "\r\n" on Windows and
    # `git mktree` would then name the file "devstatus.json\r".
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        input=None if input_text is None else input_text.encode("utf-8"),
        capture_output=True, check=check,
    )
    return subprocess.CompletedProcess(
        result.args, result.returncode,
        result.stdout.decode("utf-8", "replace"), result.stderr.decode("utf-8", "replace"),
    )


def _published(repo):
    """(document, commit sha) currently on origin/devstatus, or (None, None)."""
    if _git(repo, "fetch", "-q", "origin", TARGET_BRANCH, check=False).returncode != 0:
        return None, None
    head = _git(repo, "rev-parse", "FETCH_HEAD").stdout.strip()
    shown = _git(repo, "show", f"{head}:{FILE_NAME}", check=False)
    try:
        return json.loads(shown.stdout), head
    except json.JSONDecodeError:
        return None, head


def publish(path, repo, source_branch, attempts=3):
    """Validate the file and push it to the devstatus branch. Returns "published" or "skipped"."""
    path = pathlib.Path(path)
    document = json.loads(path.read_text(encoding="utf-8"))
    problems = validate(document)
    if problems:
        raise ValueError("devstatus.json is invalid:\n" + "\n".join(problems))

    for _ in range(attempts):
        current, parent = _published(repo)
        if not should_publish(document, current):
            return "skipped"

        blob = _git(repo, "hash-object", "-w", str(path)).stdout.strip()
        tree = _git(repo, "mktree", input_text=f"100644 blob {blob}\t{FILE_NAME}\n").stdout.strip()
        message = f"Publish dev status from {source_branch} ({document['updatedAt']})"
        parent_args = ["-p", parent] if parent else []
        commit = _git(repo, "commit-tree", tree, *parent_args, "-m", message).stdout.strip()

        # Plain push: if another run published in between, it is rejected and we re-check.
        pushed = _git(repo, "push", "-q", "origin", f"{commit}:refs/heads/{TARGET_BRANCH}", check=False)
        if pushed.returncode == 0:
            return "published"

        _, head_now = _published(repo)
        if head_now == parent:
            # Nobody else published: the push was refused for another reason
            # (permissions, a repository ruleset). Retrying won't help.
            raise RuntimeError(
                f"could not push to the {TARGET_BRANCH} branch:\n{pushed.stderr.strip()}\n"
                f"If this is a ruleset violation (GH013), exclude the '{TARGET_BRANCH}' branch from the "
                "repository ruleset or allow GitHub Actions to bypass it."
            )

    raise RuntimeError(f"could not publish: the {TARGET_BRANCH} branch kept moving")


def main(argv):
    if len(argv) != 3:
        print("usage: publish_devstatus.py <devstatus.json> <source-branch>")
        return 2
    try:
        result = publish(argv[1], pathlib.Path(argv[1]).resolve().parent, argv[2])
    except ValueError as error:
        print(error)
        return 1
    print(f"{result}: devstatus.json from {argv[2]}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
