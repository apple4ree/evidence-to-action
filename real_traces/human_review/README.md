# Single human review

The reviewer read original inputs, made judgments, drafted answers, then edited wording. Original submission is preserved. Fifteen input hashes match. Label agreement with frozen annotations: 12/15. Three disagreements remain unadjudicated; frozen gold, predictions and primary scores are unchanged.

See [analysis](analysis.md), [comparison](comparison.json), [provenance](review_provenance.json) and [citation audit](citation_audit.md). Citation corrections are suggestions, not edits to submitted answers.

After restoring public inputs, run from repository root:

```sh
python3 real_traces/human_review/analyze_submission.py
```

This compares saved labels and predictions; it runs no model inference. Single-reviewer confirmation is distinct from inter-human reproducibility and full semantic grading.
