# `pi/specs`

This folder holds **both**:

1. **`pi.csv`** — Header row only: canonical column names for PI CSV exports (Monday and manual cleanup). Input files under `pi/input/` must use these columns (order may differ; map by name).
2. **`{ItemId}.md`** — Fix specifications produced by the intake skill (e.g. `PI-2148.md`), including client URL (from `pi/input/urls/`) and suggested team/leader (from `pi/input/team/`) where applicable.

There is no separate `ref/` folder; reference and specs live together here.
