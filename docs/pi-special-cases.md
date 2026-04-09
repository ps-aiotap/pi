# PI special cases (skill context)

Use this document as PI workflow context for known product/behavior nuances that can change triage, root-cause framing, fix scope, and test expectations.

## Purpose

- Capture recurring PI edge cases that are not global coding rules.
- Help PI skills classify "bug vs expected after behavior change" correctly.
- Ensure specs and test plans include client-data correction guidance when needed.

## Case: short sell quantity sign visibility

### Behavior change

- Short sell positions are now shown using negative quantities in reporting/UI where applicable.
- Previously, those short quantities could exist in DB but were not visible in some screens/reports.

### Triage guidance

- If clients now notice buy entries (especially covering buys) that were previously hidden, first check whether this is expected visibility from the sign-display correction.
- Do not classify these as a fresh product defect by default.
- Distinguish:
  - Product logic defect (incorrect sign/math/mapping), vs
  - Historical data correction need (client/business remediation).

### Spec guidance (`pi/specs/{ItemId}.md`)

When this case applies, include:

- A note under **Summary** or **Root cause**: visibility changed due to short-sell sign handling.
- A **Data correction needed** subsection with:
  - scope (entities/accounts/securities/date range),
  - owner (client ops / AV ops / engineering support),
  - expected remediation action,
  - audit expectation.
- Acceptance criteria that separate:
  - correct product behavior post-change, and
  - completion criteria for required data cleanup.

### Test plan guidance (`pi/test-plans/{ItemId}.md`)

When this case applies, include explicit verification for:

- negative quantity display for short sells,
- covering buy sequence behavior,
- totals/valuation/report consistency after visibility change,
- no regression for long-only scenarios.

Also include a manual check for "newly visible historical entries" and expected handling path (informational vs correction workflow).

## How to maintain this file

- Add one section per recurring PI nuance with the same structure:
  1) Behavior change, 2) Triage guidance, 3) Spec guidance, 4) Test guidance.
- Keep entries concise and implementation-agnostic.
- If a nuance is retired, mark it "inactive" with date and reason instead of deleting immediately.
