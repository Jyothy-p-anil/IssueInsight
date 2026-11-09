# Journal format

- One `Module-NN/` folder per development module.
- One chapter per coherent feature, with actual current code excerpts and Git commit references.
- `DEVELOPMENT_HISTORY.md` records actual Git commits and changed files, not invented per-chat steps.
- `NOTES_INDEX.md` links the original development steps recorded in master/NOTES.md.
- `SOURCE_MAPPING.csv` maps shared files/functions to modules.
- A new commit message such as `feat(module-4): add category management` causes new top-level functions/classes/templates to appear in `Module-04/new-committed-changes.md` automatically.
- Re-running `python journal.py` refreshes the study branch without rewriting Git history.
- Source is only the committed project, never uncommitted local changes.
- A completed feature is not asserted only because a code excerpt exists.
