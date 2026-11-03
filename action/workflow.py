"""Minimal public-input validation and code aggregation; no gold imported here."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DECISIONS = {'supported', 'unsupported', 'indeterminate'}

def identifiers(case):
    return (set(case['target_action']['arguments']),
            {p['id'] for p in case['policy'] + case['tool_documentation']},
            {e['event_id'] for e in case['history']})

def issue_errors(issue, fields, policy_ids, events):
    errors = []
    if not isinstance(issue.get('field'),str) or issue['field'] not in fields: errors.append('unknown_field')
    if not isinstance(issue.get('requirement_text'), str) or not issue['requirement_text'].strip(): errors.append('missing_requirement_text')
    ps, es = issue.get('policy_ids'), issue.get('evidence_ids')
    if not isinstance(ps, list) or not ps or any(not isinstance(x, str) or x not in policy_ids for x in ps): errors.append('invalid_policy_ids')
    if not isinstance(es, list) or any(not isinstance(x, str) or x not in events for x in es): errors.append('invalid_evidence_ids')
    if not isinstance(issue.get('requirement_id'), str) or not issue['requirement_id']: errors.append('missing_requirement_id')
    ex = issue.get('exception')
    if not isinstance(ex, dict) or type(ex.get('applied')) is not bool: errors.append('invalid_exception')
    elif (not isinstance(ex.get('policy_ids'), list) or any(x not in policy_ids for x in ex['policy_ids'] if isinstance(x,str)) or any(not isinstance(x,str) for x in ex['policy_ids']) or not isinstance(ex.get('evidence_ids'), list) or any(x not in events for x in ex['evidence_ids'] if isinstance(x,str)) or any(not isinstance(x,str) for x in ex['evidence_ids']) or not isinstance(ex.get('rationale'),str)): errors.append('invalid_exception_reference')
    if not isinstance(issue.get('rationale'), str) or not issue['rationale'].strip(): errors.append('missing_rationale')
    return errors

def validate_direct(case, pred):
    fields, policies, events = identifiers(case)
    errors = []
    if not isinstance(pred, dict): return ['not_object']
    if pred.get('record_id') != case['record_id']: errors.append('wrong_id')
    if not isinstance(pred.get('decision'),str) or pred['decision'] not in DECISIONS: errors.append('invalid_decision')
    if not isinstance(pred.get('summary'),str) or not pred['summary'].strip(): errors.append('missing_summary')
    issues = pred.get('issues')
    if not isinstance(issues, list): return errors + ['issues_not_list']
    if pred.get('decision') == 'unsupported' and not issues: errors.append('unsupported_without_issue')
    if isinstance(pred.get('decision'),str) and pred['decision'] in {'supported','indeterminate'} and issues: errors.append('unexpected_issues')
    for issue in issues:
        if isinstance(issue,dict) and issue.get('relation') != 'violated': errors.append('invalid_issue_relation')
        errors.extend(issue_errors(issue, fields, policies, events) if isinstance(issue,dict) else ['invalid_issue'])
    return errors

def aggregate(case, relation):
    fields, policies, events = identifiers(case)
    errors, issues, checked = [], [], set()
    unknown = False
    if not isinstance(relation,dict): relation = {}
    if relation.get('record_id') != case['record_id']: errors.append('wrong_id')
    checks, coverage = relation.get('checks'), relation.get('coverage')
    if not isinstance(checks,list): checks=[];errors.append('checks_not_list')
    if not isinstance(coverage,list): coverage=[];errors.append('coverage_not_list')
    seen_req=set()
    for check in checks:
        if not isinstance(check,dict): errors.append('invalid_check');continue
        check_errors=issue_errors(check,fields,policies,events)
        rid=check.get('requirement_id')
        if not isinstance(rid,str) or not rid or rid in seen_req: check_errors.append('invalid_requirement_id')
        if isinstance(rid,str):seen_req.add(rid)
        if not isinstance(check.get('status'),str) or check['status'] not in {'satisfied','violated','unresolved','not_applicable'}:check_errors.append('invalid_status')
        if not isinstance(check.get('origin'),str) or check['origin'] not in {'extracted','extraction_repair'}:check_errors.append('invalid_origin')
        if check.get('status')=='violated' and isinstance(check.get('exception'),dict) and check['exception'].get('applied') is True: check_errors.append('violated_with_applied_exception')
        if check_errors:errors.extend(check_errors);continue
        checked.add(check['field'])
        if check['status']=='violated':
            issues.append({k:check[k] for k in ['requirement_id','field','requirement_text','policy_ids','evidence_ids','rationale','exception']})
            issues[-1]['relation']='violated'
        elif check['status']=='unresolved':unknown=True
    seen_fields=set()
    for item in coverage:
        if not isinstance(item,dict):errors.append('invalid_coverage');continue
        f=item.get('field')
        if not isinstance(f,str) or f not in fields or f in seen_fields:errors.append('invalid_coverage_field');continue
        seen_fields.add(f)
        status=item.get('status')
        if status=='checked':
            if f not in checked:errors.append('coverage_without_check')
        elif status=='unrestricted':
            ps=item.get('policy_ids')
            if not isinstance(ps,list) or not ps or any(not isinstance(x,str) or x not in policies for x in ps) or not item.get('rationale'):errors.append('unsupported_unrestricted_claim')
        elif status=='unknown':unknown=True
        else:errors.append('invalid_coverage_status')
    if seen_fields!=fields:errors.append('incomplete_field_coverage')
    # shortcut: public IDs prove citation existence, not semantic correctness; independent review scores that.
    decision='unsupported' if issues else 'indeterminate' if errors or unknown else 'supported'
    pred={'record_id':case['record_id'],'decision':decision,'issues':issues,'validation_errors':errors,'valid':not errors,'raw_record_id':relation.get('record_id'),'summary':relation.get('summary',''), 'extraction_repairs':sum(isinstance(x,dict) and x.get('origin')=='extraction_repair' for x in checks)}
    return pred

if __name__ == '__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('case');parser.add_argument('relation');parser.add_argument('output');args=parser.parse_args()
    Path(args.output).write_text(json.dumps(aggregate(json.loads(Path(args.case).read_text()),json.loads(Path(args.relation).read_text())),ensure_ascii=False,indent=2)+'\n')
