import json
from datetime import datetime

def load_mission_log():
    file_path = "mission_log.json"

    try:
        with open(file_path, 'r') as f:
            mission_log = json.load(f)
    except FileNotFoundError:
        # Initialize an empty mission log if no log exists
        mission_log = {
            "player_id": "agent_007",
            "missions_completed": [],
            "current_mission": None,
            "game_state": {}
        }

    return mission_log

def save_mission_log(mission_log):
    file_path = "mission_log.json"

    with open(file_path, 'w') as f:
        json.dump(mission_log, f, indent=4)

def update_mission_log(mission_log, mission_name):
    # Check if there's a mission to complete (i.e., a current mission is in progress)
    if mission_log["current_mission"] and "mission_name" in mission_log["current_mission"]:
        # Mark the current mission as completed and add it to the missions_completed list
        completed_mission = {
            "mission_name": mission_log["current_mission"]["mission_name"],
            "completed": datetime.now().isoformat()  # Record the completion timestamp
        }
        mission_log["missions_completed"].append(completed_mission)

    # Start a new mission or update the current mission
    mission_log["current_mission"] = {
        "mission_name": mission_name,
        "started": datetime.now().isoformat()  # Timestamp of when the mission started
    }

    # Save the updated mission log
    save_mission_log(mission_log)
