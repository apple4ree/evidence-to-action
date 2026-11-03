# Expanded scoring specification v1

All model outputs are scored against adjudicated gold frozen before test predictions. Scope is the annotated core violation relationships, not exhaustive recall of every normal policy requirement. No family/condition/variant metadata or gold is available to predictors.

- Schema/ID failures remain in every decision/joint denominator and appear as `invalid` in the confusion matrix. A raw Unsupported output for a Supported case counts toward false-positive rate even if malformed.
- Unsupported and Indeterminate recall require valid correct decisions. Unnecessary abstention is valid Indeterminate on gold Supported/Unsupported. Decision coverage is valid Supported/Unsupported divided by all cases.
- Blind semantic reviewers receive original public input, frozen gold, and anonymous final candidate (including summary); no method mapping. For every frozen issue unit they rate presence, affected-field attribution, applicable requirement, evidence relationship, and exception treatment. This is LLM review, not human agreement. Citation existence is validated by code; semantic support is reviewed.
- Each component accuracy divides correctly linked annotated units by all annotated units. Missing units are incorrect. Diagnostic omission counts absent annotated units. An explicitly stated but incorrect requirement is present and wrong, not omitted. Supported/Indeterminate have no violation units; their support/uncertainty rationale is assessed through summary correctness and false extra accusations.
- Full diagnostic joint: valid correct label, every annotated unit present with all four components correct, no false extra issue, and a correct summary. Annotated field-set coverage is separately computed by checking that an allowed core field set is contained in the predicted fields. Additional fields are assessed semantically for false accusations, rather than automatically rejecting a valid extra attachment. This does not prove exhaustiveness beyond the frozen gold scope.
- Explicit comparison edges use `contrast` and `invariance`. Both-endpoints-correct requires both valid correct labels. Invariance retention alone permits the same wrong label, so it is reported beside both-correct, never as accuracy. Four-variant family-all-correct is separately named. Edge scores are also stratified by intervention type; distractor-addition invariance is not pooled with policy-change invariance when describing robustness to irrelevant information.
- Report raw counts, family- and overlapping-condition-stratified counts. Bootstrap whole families, 10,000 samples, seed 20261103. Within-family proportions are equally averaged; paired method differences reuse the same sampled families. These percentile intervals describe constructed-family sampling uncertainty, not population prevalence. With very few families or ceiling results, interval bounds may be uninformative.
- No retries for malformed JSON, invalid citations or incorrect judgments. One retry maximum for technical failures with no usable model response, recorded separately.
- Gold errors discovered later retain original scoring and require method-common amendment/re-score, not selectively changed answers. Do not modify frozen files silently; new version and amendment are required.

## Semantic rating format

`review/test_semantic_ratings.json` maps every `candidate_id` to:

```json
{
 "summary_correct": true,
 "extra_false_issue_count": 0,
 "units": {
  "frozen_unit_id": {
   "present": true,
   "field_correct": true,
   "requirement_correct": true,
   "evidence_correct": true,
   "exception_correct": true
  }
 },
 "error_types": [],
 "rationale": "Specific explanation of evidence alignment or failure."
}
```

For S/I gold, units is `{}`; assess summary and any false issue. A correct label with a wrong summary fails joint diagnosis. For missing output, components are false and summary_correct false. Reviewer must not use model-specific stage outputs to infer candidate identity. After unmasking, P2 error attribution may inspect extraction and relation outputs to separate extraction omission, evidence linking, relation judgment, and code aggregation. An extraction omission repaired at stage two is recorded as repaired, not a final failure.
