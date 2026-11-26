"""Output-format validation only; never a permission correctness oracle."""
import json

class ProtocolInfrastructureError(Exception):
    pass

class InvalidStructuredOutput(ValueError):
    pass

class TokenBudgetExhausted(InvalidStructuredOutput):
    pass

def json_object(raw):
    try:
        value, _ = json.JSONDecoder().raw_decode(raw[raw.index('{'):])
        if not isinstance(value, dict):
            raise ValueError('Expected object')
        return value
    except (ValueError, TypeError) as exc:
        raise InvalidStructuredOutput('Model did not return a JSON object') from exc

def extraction(raw, valid_ids, selected_ids=None):
    value = json_object(raw)
    buttons = value.get('buttons')
    if not isinstance(buttons, list) or not buttons:
        raise InvalidStructuredOutput('Missing extracted buttons')
    ids = []
    for button in buttons:
        mid = button.get('marker_id')
        if type(mid) is not int or mid not in valid_ids or mid in ids:
            raise InvalidStructuredOutput('Invalid or duplicate extracted marker')
        if not isinstance(button.get('label'), str) or not button['label'].strip():
            raise InvalidStructuredOutput('Missing visible option label')
        if button.get('choice_level') not in ('minimum', 'broad', 'deny'):
            raise InvalidStructuredOutput('Invalid option scope label')
        if not isinstance(button.get('dimension'), str):
            raise InvalidStructuredOutput('Missing option dimension')
        ids.append(mid)
    mid = value.get('selected_marker_id')
    if type(mid) is not int or mid not in ids or mid not in (selected_ids or valid_ids):
        raise InvalidStructuredOutput('Selected marker absent from allowed extracted options')
    if value.get('selected_choice_level') not in ('minimum', 'broad', 'deny'):
        raise InvalidStructuredOutput('Missing selected scope label')
    return value

def verifier(raw, buttons, selected_ids=None):
    value = json_object(raw)
    ids = [b['marker_id'] for b in buttons]
    if type(value.get('selected_marker_id')) is not int or value['selected_marker_id'] not in (selected_ids or ids) or value['selected_marker_id'] not in ids:
        raise InvalidStructuredOutput('Verifier marker absent from current options')
    if value.get('agreement') not in ('agree', 'disagree') or value.get('choice_level') not in ('minimum', 'broad', 'deny'):
        raise InvalidStructuredOutput('Invalid verifier fields')
    return value
