# Blinded semantic review — batch 1

This is separate-context LLM semantic rating, not independent human validation. Frozen labels and criteria were retained. No predictions were run and no URLs were fetched.

## Read scope

Read `scoring_spec.md`, then `blinded_review/batch1.json`, then the complete named packets: `MAST-R01.json`, `MAST-R02.json`, `MAST-R03.json`, `MAST-R04.json`, `MAST-R05.json`, `MAST-R06.json`, and `WW-new-25-14.json`. Each packet includes its public input, frozen reference annotation and three anonymized outputs. Every file read was separate with shell output budget 30000; when the outer tool response truncated text, missing spans were reread in bounded character chunks. One attempted chunk command used unavailable `python`; the successful reread used `python3`. No private method map, predictions, responses, other experiment results or external linked material was read.

## Judgments

All 21 outputs are rated in `ratings_batch1.json`. Components are scored by their frozen criterion wording and semantic equivalence, not by reproducing the exact anchor set. No component was unscorable.

- MAST-R01: all outputs explain first-position substitution and unranked/deduplicated handoff, while retaining uncertainty about the global winning artist. Page-specific counts in outputs 2 and 3 do not assert a global winner or Supervisor access to upstream records.
- MAST-R02: all outputs trace the password to its unsupported access-token relabeling; none relies on a later 401 or blames the receiver.
- MAST-R03: all outputs identify page-limited coverage and connect it to the universal completion claim; all respect hidden-song and actor boundaries. Output 2 nevertheless classifies this as unresolved/Indeterminate. Its explicit demand for an actual counterexample or verification-policy violation conflicts with the frozen diagnosis of an observed evidence-scope promotion. Component passes do not imply correct overall decision. Evidence-semantic correctness remains true for the valid source links; contradiction is true for the explicit core-relation interpretation.
- MAST-R04: all outputs support the legitimate email request using password-only delegation and the required login field.
- MAST-R05: all outputs connect the issued login token through matching assignment to query. Outputs 1 and 2 quote the actual returned token; omitting a separate invocation quote is not a semantic failure.
- MAST-R06: outputs 1 and 2 correctly explain that a cyclic snapshot and unfiltered handoff cannot determine past playback. Output 3 fails `missing_history` and `boundary`: despite acknowledging absent earlier-cycle history in limitations, it treats position after the current song as a proved violation. Its citations establish positions and projection but cannot establish the claimed eligibility boundary, so evidence-semantic correctness is false and contradiction true. Output 2 references a prior diagnosis; this extraneous phrase supplies no scoring evidence.
- WW-new-25-14: all outputs preserve the core month/day distinction and explain the changed interval. Optional observations about the 2022 reference are qualified and do not contradict the cutoff diagnosis.

## Boundary concerns

MAST-R03 exposes a consequential distinction: truth of a universal negative is unknown, while its justification from an explicitly bounded search is unsupported. Frozen scope and scoring_spec explicitly choose the latter, so output 2 keeps its literal component passes but fails the frozen decision/core relation. This is a boundary sensitivity worth reporting, not a reason to relabel the case or rewrite a component. MAST-R06 instead asks actual membership in the played-so-far set, for which missing cycle history remains unresolved. Their different focal relations explain the label distinction; no frozen gold change was made.

`contradiction` includes an explicit explanation that contradicts the frozen core relation, not merely internal self-inconsistency. A wrong decision alone is not automatically a component failure. Core evidence sufficiency accepts alternative contextual quotes; literal locator/substring verification remains a separate mechanical check.
