# PI pipeline — optional steps

Edit this file to enable or disable optional skills without changing skill definitions.

**How agents use it:** Before running an optional step, read the flag below. If `false`, skip that step and continue the pipeline.

| Flag | Skill | Default | Purpose |
|------|-------|---------|---------|
| `business_impact` | `pi-business-impact` | **true** | Domain learning + business impact for engineering |
| `rca_human_enhancement` | `pi-rca-human-enhancement` | **false** | Enrich RCA from BA/human notes |

## Flags

```yaml
business_impact: true
rca_human_enhancement: false
```

To turn off business impact for a run, set `business_impact: false` or comment out the step in `pi/skil_run.txt`.

Per-PI override: human can say in chat *"skip business impact for this PI"* — that overrides the file for one run only.
