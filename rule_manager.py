import json
import os

RULES_FILE='rules.json'

def save_rules(rules):
    with open(RULES_FILE, 'w') as file:
        json.dump(rules, file, indent=4)

def load_rules():
    if os.path.exists(RULES_FILE):
        with open(RULES_FILE, 'r') as file:
            return json.load(file)
    return {}