from basecamp import *


def test_parse_points():
    s = "some long line of text like this (255)"
    ss = "some long line of text like this (0)"
    assert parse_points(s) == 255
    assert parse_points(ss) == 0


def test_get_points_available():
    li = [
        {'points': 10},
        {'points': 20},
        {'points': 30},
        {'points': 40}
    ]
    assert get_points_available(li) == 100


def test_parse_user_from_json():
    dump = {
        "account_id": "4514340",
        "teams": [
            {
                "assigned_to": None,
                "completed_tasks": [],
                "consolidated_tasks": [],
                "name": "new_team",
                "points_completed": 0,
                "points_required": 0,
                "project_id": 17323445,
                "todoset_id": 2717518684
            },
            {
                "assigned_to": None,
                "completed_tasks": [],
                "consolidated_tasks": [
                    {
                        "assignees": [],
                        "due_on": None,
                        "id": 2714614743,
                        "points": 2,
                        "status": "active",
                        "title": "TEST TASK F (2)"
                    },
                    {
                        "assignees": [],
                        "due_on": None,
                        "id": 2714614957,
                        "points": 2,
                        "status": "active",
                        "title": "TEST TASK H (2)"
                    },
                    {
                        "assignees": [],
                        "due_on": None,
                        "id": 2714626468,
                        "points": 2,
                        "status": "active",
                        "title": "TEST TASK I (2)"
                    },
                    {
                        "assignees": [],
                        "due_on": None,
                        "id": 2714626577,
                        "points": 1,
                        "status": "active",
                        "title": "TEST TASK J (1)"
                    },
                    {
                        "assignees": [],
                        "due_on": None,
                        "id": 2714626681,
                        "points": 1,
                        "status": "active",
                        "title": "TEST TASK K (1)"
                    },
                    {
                        "assignees": [],
                        "due_on": None,
                        "id": 2714626799,
                        "points": 2,
                        "status": "active",
                        "title": "TEST TASK L (2)"
                    },
                    {
                        "assignees": [],
                        "due_on": None,
                        "id": 2714626881,
                        "points": 1,
                        "status": "active",
                        "title": "TEST TASK M (1)"
                    }
                ],
                "name": "TEST",
                "points_completed": 0,
                "points_required": 11,
                "project_id": 17289546,
                "todoset_id": 2709742084
            },
            {
                "assigned_to": "Race, Dimitri, Phuc",
                "completed_tasks": [],
                "consolidated_tasks": [
                    {
                        "assignees": [],
                        "due_on": None,
                        "id": 2709190243,
                        "points": 10,
                        "status": "active",
                        "title": "Logos, pictures, and screenshots complete (10)"
                    },
                    {
                        "assignees": [],
                        "due_on": None,
                        "id": 2709191813,
                        "points": 50,
                        "status": "active",
                        "title": "Preliminary demo (50)"
                    },
                    {
                        "assignees": [],
                        "due_on": None,
                        "id": 2709193873,
                        "points": 20,
                        "status": "active",
                        "title": "Team summary (20)"
                    }
                ],
                "name": "Presentation",
                "points_completed": 0,
                "points_required": 80,
                "project_id": 17286974,
                "todoset_id": 2709183133
            },
            {
                "assigned_to": "Yanxun, Nicholas",
                "completed_tasks": [],
                "consolidated_tasks": [
                    {
                        "assignees": [],
                        "due_on": None,
                        "id": 2709218401,
                        "points": 30,
                        "status": "active",
                        "title": "Feature complete - Profile (30)"
                    },
                    {
                        "assignees": [],
                        "due_on": None,
                        "id": 2709218832,
                        "points": 40,
                        "status": "active",
                        "title": "Completed feature merged to master - Profile (40)"
                    },
                    {
                        "assignees": [],
                        "due_on": None,
                        "id": 2709219556,
                        "points": 20,
                        "status": "active",
                        "title": "CodeClimate passes - Profile (20)"
                    },
                    {
                        "assignees": [],
                        "due_on": None,
                        "id": 2709219140,
                        "points": 30,
                        "status": "active",
                        "title": "Tests complete - Profile (30)"
                    }
                ],
                "name": "User Profile",
                "points_completed": 0,
                "points_required": 120,
                "project_id": 17211956,
                "todoset_id": 2693172484
            },
            {
                "assigned_to": "Andrew",
                "completed_tasks": [],
                "consolidated_tasks": [
                    {
                        "assignees": [],
                        "due_on": None,
                        "id": 2709203913,
                        "points": 30,
                        "status": "active",
                        "title": "Feature complete - DLM (30)"
                    },
                    {
                        "assignees": [],
                        "due_on": None,
                        "id": 2709205026,
                        "points": 40,
                        "status": "active",
                        "title": "Completed feature merged to master - DLM (40)"
                    },
                    {
                        "assignees": [],
                        "due_on": None,
                        "id": 2709209496,
                        "points": 30,
                        "status": "active",
                        "title": "Tests complete - DLM (30)"
                    },
                    {
                        "assignees": [],
                        "due_on": None,
                        "id": 2709211698,
                        "points": 20,
                        "status": "active",
                        "title": "CodeClimate passes - DLM (20)"
                    }
                ],
                "name": "Dark/Light Mode",
                "points_completed": 0,
                "points_required": 120,
                "project_id": 17211953,
                "todoset_id": 2693171970
            },
            {
                "assigned_to": "Jason",
                "completed_tasks": [],
                "consolidated_tasks": [
                    {
                        "assignees": [],
                        "due_on": None,
                        "id": 2709347203,
                        "points": 30,
                        "status": "active",
                        "title": "Feature complete - Deadlines (30)"
                    },
                    {
                        "assignees": [],
                        "due_on": None,
                        "id": 2709347644,
                        "points": 40,
                        "status": "active",
                        "title": "Completed feature merged to master - Deadlines (40)"
                    },
                    {
                        "assignees": [],
                        "due_on": None,
                        "id": 2709348437,
                        "points": 30,
                        "status": "active",
                        "title": "Tests complete - Deadlines (30)"
                    },
                    {
                        "assignees": [],
                        "due_on": None,
                        "id": 2709348956,
                        "points": 20,
                        "status": "active",
                        "title": "CodeClimate passes - Deadlines (20)"
                    }
                ],
                "name": "Task Deadlines",
                "points_completed": 0,
                "points_required": 120,
                "project_id": 17158764,
                "todoset_id": 2681080631
            },
            {
                "assigned_to": "Kaylen, Johnny, Austin",
                "completed_tasks": [],
                "consolidated_tasks": [
                    {
                        "assignees": [],
                        "due_on": None,
                        "id": 2709352787,
                        "points": 40,
                        "status": "active",
                        "title": "Completed feature merged to master - UI (40)"
                    },
                    {
                        "assignees": [],
                        "due_on": None,
                        "id": 2709353375,
                        "points": 30,
                        "status": "active",
                        "title": "Tests complete - UI (30)"
                    },
                    {
                        "assignees": [],
                        "due_on": None,
                        "id": 2709353971,
                        "points": 20,
                        "status": "active",
                        "title": "CodeClimate passes - UI (20)"
                    }
                ],
                "name": "UI",
                "points_completed": 0,
                "points_required": 90,
                "project_id": 17149883,
                "todoset_id": 2679853458
            }
        ]
    }

    parsed_users = {
        "Andrew": {
            "points_completed": 0,
            "points_required": 120,
            "productivity": 0.0,
            "team": "Dark/Light Mode"
        },
        "Austin": {
            "points_completed": 0,
            "points_required": 90,
            "productivity": 0.0,
            "team": "UI"
        },
        "Dimitri": {
            "points_completed": 0,
            "points_required": 80,
            "productivity": 0.0,
            "team": "Presentation"
        },
        "Jason": {
            "points_completed": 0,
            "points_required": 120,
            "productivity": 0.0,
            "team": "Task Deadlines"
        },
        "Johnny": {
            "points_completed": 0,
            "points_required": 90,
            "productivity": 0.0,
            "team": "UI"
        },
        "Kaylen": {
            "points_completed": 0,
            "points_required": 90,
            "productivity": 0.0,
            "team": "UI"
        },
        "Nicholas": {
            "points_completed": 0,
            "points_required": 120,
            "productivity": 0.0,
            "team": "User Profile"
        },
        "Phuc": {
            "points_completed": 0,
            "points_required": 80,
            "productivity": 0.0,
            "team": "Presentation"
        },
        "Race": {
            "points_completed": 0,
            "points_required": 80,
            "productivity": 0.0,
            "team": "Presentation"
        },
        "Yanxun": {
            "points_completed": 0,
            "points_required": 120,
            "productivity": 0.0,
            "team": "User Profile"
        }
    }
    bc = Basecamp("", "")
    assert parsed_users == bc.parse_user_from_json(dump)
