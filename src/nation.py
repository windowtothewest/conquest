from typing import List, Dict
import asciichartpy as acp
import numpy as np

""" To do:
[ ] Implement system for events to be provided that alter nation scores
[ ] Implement system to manage taxation and budgeting
[ ] Implement system to manage military and warfare with other nations
"""

nation_types = {
    "Anarchy" : {"political_freedom": 1, "economy": 1, "civil_rights": 1},
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
        
        self.civic_score_history = {
            "political_freedom": [float(self.political_freedom_score)],
            "economy": [float(self.economy_score)],
            "civil_rights": [float(self.civil_rights_score)],
        }


        self.encountered_events = set()
    
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

    def overton_window_calculator(self):
        """ This function calculates the Overton Window of the nation based on the political freedom, economy, and civil rights scores."""
        pef = self.political_freedom_score
        ef = self.economy_score
        pof = self.civil_rights_score
        current_nation_type = self.nation_type
        if pef <= 0.33 and ef <= 0.33 and pof <= 0.33: # Bottom of Personal Freedom Range
            new_nation_type = "Psychotic Dictatorship"
        elif pef <= 0.33 and ef <= 0.33 and (pof > 0.33 and pof <= 0.66):
            new_nation_type = "Authoritarian Democracy"
        elif pef <= 0.33 and ef <= 0.33 and pof > 0.66:
            new_nation_type = "Tyranny by Majority"
        elif pef <= 0.33 and (ef > 0.33 and ef <= 0.66) and pof <= 0.33:
            new_nation_type = "Iron Fist Consumerists"
        elif pef <= 0.33 and ef > 0.66 and pof <= 0.33:
            new_nation_type = "Corporate Police State"
        elif pef <= 0.33 and (ef > 0.33 and ef <= 0.66) and (pof > 0.33 and pof <= 0.66):
            new_nation_type = "Moralistic Democracy"
        elif pef <= 0.33 and (ef > 0.33 and ef <= 0.66) and pof > 0.66:
            new_nation_type = "Conservative Democracy"
        elif pef <= 0.33 and ef > 0.66 and (pof > 0.33 and pof <= 0.66):
            new_nation_type = "Right-wing Utopia"
        elif pef <= 0.33 and ef > 0.66 and pof > 0.66:
            new_nation_type = "Free Wing Paradise"
        elif (pef > 0.33 and pef <= 0.66) and ef <= 0.33 and pof <= 0.33: # Middle of Personal Freedom Range
            new_nation_type = "Corrupt Dictatorship"
        elif (pef > 0.33 and pef <= 0.66) and ef <= 0.33 and (pof > 0.33 and pof <= 0.66):
            new_nation_type = "Democratic Socialists"
        elif (pef > 0.33 and pef <= 0.66) and ef <= 0.33 and pof > 0.66:
            new_nation_type = "Liberal Democratic Socialists"
        elif (pef > 0.33 and pef <= 0.66) and (ef > 0.33 and ef <= 0.66) and pof <= 0.33:
            new_nation_type = "Father Knows Best State"
        elif (pef > 0.33 and pef <= 0.66) and ef > 0.66 and pof <= 0.33:
            new_nation_type = "Compulsory Consumerist State"
        elif (pef > 0.33 and pef <= 0.66) and (ef > 0.33 and ef <= 0.66) and (pof > 0.33 and pof <= 0.66):
            new_nation_type = "Inoffensive Centrist Democracy"
        elif (pef > 0.33 and pef <= 0.66) and (ef > 0.33 and ef <= 0.66) and pof > 0.66:
            new_nation_type = "New York Times Democracy"
        elif (pef > 0.33 and pef <= 0.66) and ef > 0.66 and (pof > 0.33 and pof <= 0.66):
            new_nation_type = "Capitalist Paradise"
        elif (pef > 0.33 and pef <= 0.66) and ef > 0.66 and pof > 0.66:
            new_nation_type = "Corporate Bordello"
        elif pef > 0.66 and ef <= 0.33 and pof <= 0.33: # Top of Personal Freedom Range
            new_nation_type = "Iron Fist Socialist"
        elif pef > 0.66 and ef <= 0.33 and (pof > 0.33 and pof <= 0.66):
            new_nation_type = "Scandinavian Liberal Paradise"
        elif pef > 0.66 and ef <= 0.33 and pof > 0.66:
            new_nation_type = "Leftwing Utopia"
        elif pef > 0.66 and (ef > 0.33 and ef <= 0.66) and pof <= 0.33:
            new_nation_type = "Libertarian Police State"
        elif pef > 0.66 and ef > 0.66 and pof <= 0.33:
            new_nation_type = "Benevolent Dictatorship"
        elif pef > 0.66 and (ef > 0.33 and ef <= 0.66) and (pof > 0.33 and pof <= 0.66):
            new_nation_type = "Left-Leaning College State"
        elif pef > 0.66 and (ef > 0.33 and ef <= 0.66) and pof > 0.66:
            new_nation_type = "Civil Rights Lovefest"
        elif pef > 0.66 and ef > 0.66 and (pof > 0.33 and pof <= 0.66):
            new_nation_type = "Capitalizt"
        elif pef > 0.66 and ef > 0.66 and pof > 0.66:
            new_nation_type = "Anarchy"
        
        if new_nation_type != current_nation_type:
            print(f"Your nation has shifted from {current_nation_type} to {new_nation_type}.")
            self.nation_type = new_nation_type




def main():
    pass

if __name__ == "__main__":
    main()