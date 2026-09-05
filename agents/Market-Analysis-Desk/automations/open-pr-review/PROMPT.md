Check GitHub (authenticated as prosmoon-hash) for open pull requests this account can see, including PRs in any repos that appear later. If there are none, stay silent and do not message the user.

If any open PR has not already been reviewed, actually read the full diff and the surrounding architecture. Never approve, merge, or edit code. Report findings to the user ranked by severity. Each finding must point at a specific file and line with a reason. Look for security issues, broken edge cases, missing tests, and contradictions with existing architecture. If a PR is clean, send a short "no issues found" for that PR rather than inventing problems. Never invent issues.

Once a concrete repo is known, review that repo's open PRs first. If GitHub auth fails, say so once; if it keeps failing, pause this routine and tell the user to reconnect.
