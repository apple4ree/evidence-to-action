# Scoring specification

Root supplies case-level gold before freeze. Evaluate only visible-record evidential support and localization of initial source, transformation and reuse. Gold must distinguish supported factual reuse, legitimate search/clarification, unsupported changes, and indeterminate missing evidence. Full hidden policy compliance is outside the available record.

For each method and phase report: decision accuracy/confusion, Unsupported recall, Supported false-positive rate, Indeterminate accuracy and unnecessary abstention, with raw denominators. Also report first-source, transformation, reuse localization and scope-link (entity/time/condition/source/coverage) semantic correctness. Empty chains may be correct for cases without a transformation. Do not infer exhaustive lineage recall from selected core annotations. Report diagnosis jointly only in addition to components. Invalid JSON/references stay in denominator and are separate from semantic uncertainty.

Reviewers should not see method identity. Multiple adjacent raw lines or equivalent event bundles can express one correct relation; compare meaning and actual provenance rather than equality of sets. A correct decision with a wrong source/link remains a diagnostic error. Report D1-only and P2-only correct cases, D2 fixes/regressions, and P2 extraction/link/relation/synthesis errors if observed. If no divergence appears, retain the tie. No expansion until a gap is found.

Costs: unique sessions, effective per-method sessions (D2 includes reused D1), observable tokens/time; unknown model snapshot/cost stay unknown. Analysis is descriptive because only two exploration and three heldout source episodes are included. No unsupported confidence or prevalence claims.

## Frozen semantic rating fields

Each anonymous final candidate receives booleans `first_source_correct`, `transformation_correct`, `reuse_correct`, `scope_links_correct`, `uncertainty_correct`, `rationale_correct`, plus `unsupported_extra_claims` integer and an evidence-specific rationale. These score the selected core chain, allowing equivalent source bundles; locating an earlier root or a later observed state is valid if its role is correctly identified. Unsupported recall on the heldout set is undefined (0 gold errors); missing-policy uncertainty must not turn legitimate inquiry into a forced Indeterminate. Final joint requires schema-valid correct label and all six booleans with zero unsupported extras.
