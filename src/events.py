import os
import json
import asciichartpy as acp
from nation import Nation
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
    return response

class Event:
    def __init__(self, name:str, type:str, description:str, choices:List[Dict]):
        self.name = name
        self.type = type
        assert self.type in ["political", "economic", "military"], "Invalid event type. Must be political, economic, or military."
        self.description = description
        self.choices = choices
        self.effects = {}
        for index, choice in enumerate(choices):
            self.effects[str(index+1)] = {
                "political_freedom": choice["option_effects"]["political_freedom"],
                "economy": choice["option_effects"]["economy"],
                "civil_rights": choice["option_effects"]["civil_rights"],
            }
    
    def apply_effects(self, nation:Nation, response:str):
        if self.type == "political":
            nation.political_freedom_score += self.effects[response]["political_freedom"]
            nation.economy_score += self.effects[response]["economy"]
            nation.civil_rights_score += self.effects[response]["civil_rights"]
            if nation.political_freedom_score < 0:
                nation.political_freedom_score = 0
            elif nation.political_freedom_score > 1:
                nation.political_freedom_score = 1
            if nation.economy_score < 0:
                nation.economy_score = 0
            elif nation.economy_score > 1:
                nation.economy_score = 1
            if nation.civil_rights_score < 0:
                nation.civil_rights_score = 0
            elif nation.civil_rights_score > 1:
                nation.civil_rights_score = 1
            nation.civic_score_history["political_freedom"].append(float(nation.political_freedom_score))
            nation.civic_score_history["economy"].append(float(nation.economy_score))
            nation.civic_score_history["civil_rights"].append(float(nation.civil_rights_score))
        elif self.type == "economic": # Not yet implemented
            raise NotImplementedError("Economic events are not yet implemented.")
            nation.budget += self.effects[response]["budget"]
            nation.tax_rate += self.effects[response]["tax_rate"]
            nation.gdp += self.effects[response]["gdp"]
        elif self.type == "military": # Not yet implemented
            raise NotImplementedError("Military events are not yet implemented.")
            nation.military_budget += self.effects[response]["military_budget"]
            nation.military_is_hostile += self.effects[response]["military_is_hostile"]
            nation.military_population += self.effects[response]["military_population"]
    
    def respond_to_event(self, nation):
        print(self.description.replace('[Nation Name]', nation.name))
        for index, choice in enumerate(self.choices):
            print(f"{index+1}. {choice['option_description']}")
        response = survey_question("How will you choose to respond?", [str(i+1) for i in range(len(self.choices))])
        self.apply_effects(nation=nation, response=response)
        nation.overton_window_calculator()

        print(f"Political freedom score: {nation.political_freedom_score}")
        print("Here is the progression of your political freedoms.")
        print(acp.plot(nation.civic_score_history["political_freedom"]))
        
        print(f"Economic score: {nation.economy_score}")
        print("Here is the progression of your economic freedoms.")
        print(acp.plot(nation.civic_score_history["economy"]))
        
        print(f"Civil rights score: {nation.civil_rights_score}")
        print("Here is the progression of your civil rights.")
        print(acp.plot(nation.civic_score_history["civil_rights"]))
        

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