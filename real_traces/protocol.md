# Real-trace comparison, pre-prediction protocol

15 selected published-log cases, 14 source-run groups. These are error-oriented curated exploration cases, not a random deployment sample or an independent heldout generalization benchmark. The original synthetic evaluation remains separate.

D1: one direct diagnosis session. D2: direct diagnosis reused, followed by one fresh critique/revision session. P2: one requirement extraction session, followed by one fresh evidence/relation session and deterministic composition. Total 4 unique fresh sessions per case, 60 sessions. Sessions may involve internal tool/model exchanges, so this is not a claim of 60 API calls or equal computational cost.

All methods receive the exact same original public input and neutral focal relation. D2 receives D1 prediction; P2 receives its own extraction prediction. No gold annotations, author explanations, source suffix, or method-specific additional context is provided. Each fresh child reads only its prepared request file. Request and response hashes, runtime task ID, settings and observable usage are saved. Exact immutable model ID and monetary cost remain null if not available.

Core task: diagnose the focal support relation, not every possible tool contract or full provenance graph. Labels and semantic components in gold are fixed before inference. Meaning is scored separately from literal reference validity. Alternative reasonable field assignments are not penalized when the same relation is accurately described. No post-result change to gold is silently applied.

Primary reports: decision confusion matrix, Unsupported recall, Supported false-positive rate, Indeterminate accuracy, unnecessary abstention; diagnosis of focal relation, evidence connection and overall joint correctness. Show counts per case, source dataset, and group. No independence assumption over same-run cases. Cost: active native-session elapsed time if available, actual reported token increments, response bytes; preparation-to-collection intervals separately, not model latency.

Retry: at most one fresh technical retry only when no usable final response is produced (transport/process failure). Wrong decisions, bad evidence, malformed JSON and reference errors are outcomes, not reasons to retry. Preserve every original response and failure. No prompt edits after evaluation begins. If a reference-validation implementation bug is discovered, preserve old results and apply the same fix to all methods in a separately versioned re-score.

Semantic review: compare anonymized predictions to frozen core components and original records. Judge whether the focal conclusion and cited support relation are correct. Preserve component ratings and reviewer provenance. LLM semantic ratings are not human annotation agreement. This turn's collection/annotation workers must not serve as isolated diagnostic predictors.
