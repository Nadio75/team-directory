#!/usr/bin/env python3
"""Simple Team Directory CLI."""

import json

def load_team(filepath="team.json"):
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {filepath} not found.")
        return []

def display_team(team):
    for member in team:
        print(f"{member['name']} - {member['role']} ({member['email']})")

def search_by_name(team, query):
    return [m for m in team if query.lower() in m["name"].lower()]

if __name__ == "__main__":
    team = load_team()
    display_team(team)
    print(f"\nTotal members: {len(team)}")

    results = search_by_name(team, "a")
    print("\nSearch results for 'a':")
    display_team(results)