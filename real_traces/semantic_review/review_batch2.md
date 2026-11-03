# Blinded semantic review, batch 2

This is a separate-context LLM semantic rating, not independent human validation. The frozen reference labels and semantic criteria were retained. No predictions were run and no URLs were fetched.

## Read scope

Read `scoring_spec.md`, `blinded_review/batch2.json`, and the complete named packets: `WW-new-43-12.json`, `WW-new-4-14.json`, `WW-new-26-30.json`, `AHN01.json`, `AHN04.json`, `AHN07.json`, `AHN08.json`, and `AHN09.json`. Each packet was read separately with a 30,000-token command budget. The enclosing tool output truncated portions of two longer packets, so the omitted WW-new-4-14 history item 12 and WW-new-26-30 history items 13–17 were subsequently read in full as chunks of those same files. A first attempted chunk command used unavailable `python`; it was rerun successfully using `python3`.

Did not read private_method_map.json, unblinded predictions, responses, other experiment results, or source URLs. Only the anonymized outputs within the authorized packets were rated.

## Method and results

Rated all 24 outputs against every frozen semantic component. Semantic equivalence and valid alternative evidence were accepted; no exact anchor set or quote length was required. The resulting ratings contain 48 component passes, 6 failures, and no unscorable components. All 24 outputs have semantically appropriate evidence for the core diagnosis and no contradiction of the core relation. These evidence flags do not erase missing components. Decision accuracy and mechanical quote-location validation remain separate aggregation checks.

All three outputs pass all components for WW-new-43-12, WW-new-4-14, WW-new-26-30, AHN01, AHN04, and AHN07. In WW-new-43-12, output_1 satisfies time_or_boundary through the missing full interval coverage, even though it does not discuss the Today/May2023 gap. In WW-new-26-30, an earlier FileSurfer save receipt is a valid alternative to the final receipt anchor.

AHN08 output_1, output_2, and output_3 fail normal_value. They explain the assumed current/shared-directory mapping and correctly avoid inferring a wrong location, but none recognizes that 9 originates in the word-count tool output. Output_1 quotes the target sentence containing 9, which alone is not a provenance link or an explanation of its supported reuse. All three pass location_gap and uncertainty. Their evidence correctly supports the unresolved location diagnosis; omission of the value provenance is a missing required component, not a contradictory claim.

AHN09 output_1, output_2, and output_3 fail file_link. All correctly compare the returned text with the bullet-formatted report, so content_preservation passes. None connects the located goals.txt and academic_venture context to the read/report. Output_3 names academic_venture/goals.txt in a requirement but gives neither an explanatory linkage nor evidence of the located file and directory. Mentioning the path without making the required connection is insufficient. The supplied read and target quotes remain semantically correct evidence for content preservation.

## Boundary concerns retained separately

AHN08's public focal relation is file location, while normal_value additionally requires value provenance. AHN09's public focal relation asks about quoted content support, while file_link additionally requires the located-file/directory relationship. The omissions are therefore understandable under a narrow reading of the public focal prompts. Nevertheless, the explicit frozen criteria require both additional components, so these are scored fail consistently across all three outputs, without changing the labels or rubric. These are scope-alignment concerns for future benchmark revisions, not grounds for retroactively relaxing this scoring.

AHN07 is rated against recorded post_tweet execution and returned post object, not external Twitter state or authorization. AHN04 preserves account-mapping uncertainty rather than treating john/Robert naming differences as a contradiction. WW-new-26-30 assesses a request for inspection, not successful identity verification or efficiency. These frozen boundaries are sufficiently clear to score without unscorable entries.
