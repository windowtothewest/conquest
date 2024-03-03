import os
import json
from typing import List, Dict

def survey_question(question:str, choices:List[str]):
    print(question)
    print("Available choices: ")
    for choice in choices:
        print(f"{choice} \n") 
    valid_response = False
    while valid_response == False:
        response = input("Your choice: ")
        if response in choices:
            valid_response = True
            return response
        else:
            print("Invalid choice. Please try again.")

class Event:
    def __init__(self, name:str, type:str, description:str, choices:Dict, effects:Dict):
        self.name = name
        self.type = type
        assert self.type in ["political", "economic", "military"], "Invalid event type. Must be political, economic, or military."
        self.description = description
        self.choices = choices
        self.effects = effects
    
    def respond_to_event(self, nation):
        print(self.description)
        for choice in self.choices.keys():
            print(f"{choice} \n")
        response = survey_question("How will you choose to respond?", list(self.choices.keys()))
        self.apply_effects(nation, response)
    
    def apply_effects(self, nation, response:str):
        if self.type == "political":
            nation.political_freedom_score += self.effects[response]["political_freedom"]
            nation.economy_score += self.effects[response]["economy"]
            nation.civil_rights_score += self.effects[response]["civil_rights"]
        elif self.type == "economic": # Not yet implemented
            nation.budget += self.effects[response]["budget"]
            nation.tax_rate += self.effects[response]["tax_rate"]
            nation.gdp += self.effects[response]["gdp"]
        elif self.type == "military": # Not yet implemented
            nation.military_budget += self.effects[response]["military_budget"]
            nation.military_is_hostile += self.effects[response]["military_is_hostile"]
            nation.military_population += self.effects[response]["military_population"]

def event_from_json(path:str):
    assert os.path.exists(path), "Invalid path. File does not exist."
    with open(path, "r") as file:
        event_data = json.load(file)
    this_event = Event(
        name = event_data["event_title"],
        type = event_data["event_type"],
        description = event_data["event_description"],
        choices = event_data["event_options"],
    )
    return this_event

def main():
    pass

if __name__ == '__main__':
    main()