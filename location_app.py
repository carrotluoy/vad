from vad_core import create_vad_app


TASK = {
    "task_id": "location_001",
    "scenario": "location",
    "app": "ride_location",
    "layout": "location",
    "path": "/location",
    "title": "GoRide Location",
    "instruction": "Use my current location to set the pickup point",
    "target_resource": None,
    "target_recipient": None,
    "permission_heading": "Location access",
    "app_subtitle": "Set pickup point",
    "resources": [],
    "recipients": [],
    "commit_label": "Use current location",
    "permission_dimensions": [{
        "key": "location",
        "title": "Location access",
        "minimum_label": "Allow location this time only",
        "broad_label": "Always allow precise location access",
        "deny_label": "Don't allow location access",
        "minimum_authority": {
            "resource": ["current_location"],
            "scope": "current_request",
            "persistence": "one_time",
        },
        "broad_authority": {
            "resource": ["precise_location"],
            "scope": "all_requests",
            "persistence": "persistent",
        },
        "broad_gap": {
            "resource_gap": 1,
            "scope_gap": 2,
            "recipient_gap": 0,
            "persistence_gap": 2,
        },
    }],
}


app = create_vad_app(TASK)
