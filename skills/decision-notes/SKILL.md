---
name: Decision notes
description: >-
  Use this when recording a decision after a finished task, or when a new task
  might match an older decision and should be surfaced first.
---
# Decision notes

After a finished task that involved a real choice, write a short markdown note. Notes are decisions with reasoning, not summaries of what happened.

## File
- One note per file, named `NNNN-slug.md` (zero-padded, monotonic).
- Never delete or rewrite an existing note. If the decision changed, add a new note that names the one it supersedes and links back.

## Body
- Title: `NNNN — short decision`
- Date
- Related: link at least one older note (the root note is the only exception)
- Supersedes: `NNNN` or `—`
- Chose
- Why
- Rejected
- Unsure

## Before new work
If a new task resembles an existing note, surface that note (chose + why, plus the file link) before work starts.

## Current truth
A note is current if no later note lists it under Supersedes. Do not edit an old note to mark it superseded.
