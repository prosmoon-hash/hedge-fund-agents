# 0002 — Never rewrite a decision; supersede it

Date: 2026-08-29
Related: [0001](./0001-decision-notes-live-in-ops.md)
Supersedes: —

## Chose
Existing notes are frozen. If a decision changes, add a new note that names the one it supersedes and links back. Do not edit, delete, or restamp the old file (including its status).

## Why
A rewritten note hides the fact that we changed our mind. The chain (new note → old note) is the history. Current truth is whichever note has not been superseded.

## Rejected
- Editing an old note in place (loses the previous reasoning)
- A mutable `CURRENT.md` index (that is a rewrite by another name)
- Marking the old file `superseded` (that would be a rewrite of the old file)

## Unsure
- How we will scan for "current" notes once the folder is large (filename order plus `Supersedes:` on newer notes, until that breaks down)
