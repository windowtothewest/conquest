from typing import List, Dict
import numpy as np

""" To do:
[ ] Implement system for events to be provided that alter nation scores
[ ] Implement system to manage taxation and budgeting
[ ] Implement system to manage military and warfare with other nations
"""

nation_types = {
    "Anarchic" : {"political_freedom": 1, "economy": 1, "civil_rights": 1},
    "Libertarian" : {"political_freedom": .8, "economy": .8, "civil_rights": .8},
    "Capitalist" : {"political_freedom": .6, "economy": .8, "civil_rights": .6},
    "Liberal" : {"political_freedom": .9, "economy": .3, "civil_rights": .5},
    "Centrist" : {"political_freedom": .5, "economy": .5, "civil_rights": .5},
    "Conservative" : {"political_freedom": .2, "economy": .7, "civil_rights": .4},
    "Socialist" : {"political_freedom": .7, "economy": .05, "civil_rights": .1},
    "Authoritarian" : {"political_freedom": .1, "economy": .1, "civil_rights": .1},
    "Tyrannical" : {"political_freedom": 0, "economy": 0, "civil_rights": 0},
    "Random" : {"political_freedom": np.random.rand(1), "economy": np.random.rand(1), "civil_rights": np.random.rand(1)},
}

nation_history = {
    "segregationalist" : "Violent Segregationists",
    "tribe" : "Recently Discovered Undiscovered Tribe",
    "sacker" : "Sackers and Salvagers",
    "isolationist" : "Like-Minded Isolationists",
    "pioneer" : "Plucky, Malnourished Pioneers",
    "refugee" : "Ethnic Cleansing Refugees",
    "wrangler" : "Diplomatic Homeland Wranglers",
    "survivor" : "Civil Bloodbath Survivors",
    "pilgrim" : "Long-Suffering But Still Optimistic Pilgrims",
}

# This dictionary dictates how much the nation score is altered if chosen
nation_history_score_alterations = { 
    "segregationalist" : {"political_freedom": -.2, "economy": -.1, "civil_rights": -.5},
    "tribe" : {"political_freedom": .1, "economy": .1, "civil_rights": .1},
    "sacker" : {"political_freedom": -.5, "economy": .5, "civil_rights": -.5},
    "isolationist" : {"political_freedom": -.5, "economy": .5, "civil_rights": -.5},
    "pioneer" : {"political_freedom": -.5, "economy": .5, "civil_rights": -.5},
    "refugee" : {"political_freedom": -.5, "economy": .5, "civil_rights": -.5},
    "wrangler" : {"political_freedom": -.5, "economy": .5, "civil_rights": -.5},
    "survivor" : {"political_freedom": -.5, "economy": .5, "civil_rights": -.5},
    "pilgrim" : {"political_freedom": -.5, "economy": .5, "civil_rights": -.5},
}

class Nation:
    def __init__(self, name:str, leader:str, capital:str):
        self.name = name
        self.leader = leader
        self.capital = capital

        self.nation_type = None
        self.civilian_population = 1000
        self.length_of_existence = 0

        self.military_participiation = .1 # Bounded 0 to 1
        self.military_population = int(self.military_participiation * self.civilian_population)
        
        self.political_freedom_score = .5 # Bounded 0 to 1
        self.economy_score = .5 # Bounded 0 to 1
        self.civil_rights_score = .5 # Bounded 0 to 1
    
    @staticmethod
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

    def initial_survey(self):
        # Initializing the base nation scores based on nation type
        print("Choose your nation type: ")
        self.nation_type = self.survey_question(
            question = "What type of nation would you like to create?",
            choices = nation_types.keys()
        )
        self.political_freedom_score = nation_types[self.nation_type]["political_freedom"]
        self.economy_score = nation_types[self.nation_type]["economy"]
        self.civil_rights_score = nation_types[self.nation_type]["civil_rights"]
        print(f"Your nation will begin as: {self.nation_type}. Interesting choice.")
    
    def respond_to_event(self, event):
        event.respond_to_event(self)

def main():
    pass

if __name__ == "__main__":
    main()