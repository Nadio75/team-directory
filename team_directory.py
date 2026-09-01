#!/usr/bin/env python3
"""Simple Team Directory CLI."""

import json

def load_team(filepath="team.json"):
    with open(filepath, "r") as f:
        return json.load(f)

def display_team(team):
    for member in team:
        print(f"{member['name']} - {member['role']} ({member['email']})")

if __name__ == "__main__":
    team = load_team()
    display_team(team)