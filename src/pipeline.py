from nation import Nation
from events import Event
import os
import pickle
import argparse

def runtime(load_existing_save=False, existing_save_path=None):
    if load_existing_save and (existing_save_path is not None):
        assert os.path.exists(existing_save_path), "Invalid path to existing save file."
        try:
            with open(load_existing_save, "rb") as file:
                nation_instance = pickle.load(file)
                assert isinstance(nation_instance, Nation), "Invalid save file. Must be a Nation object."
        except FileNotFoundError:
            print("No existing save file found.")
    else:
        # Instantiate new Nation object
        nation_name = input("What will you call your nation? ")
        nation_leader = input("Who will be the leader of your nation? ")
        nation_capital = input("What will be the capital of your nation? ")
        nation_instance = Nation(nation_name, nation_leader, nation_capital)
        nation_instance.initial_survey()
        print(f"Your nation has been created. Welcome to the world stage, {nation_leader}")
    
    # Main game loop
    game_continue = True
    while game_continue:
        print("What would you like to do?")
        print("1. Respond to an event.")
        print("2. Save and exit")
        print("3. Exit without saving")
        response = str(input("Your choice: "))
        if response == "1":
            # Respond to an event
            pass
        elif response == "2":
            # Save and exit
            with open(f"{nation_instance.name}.pkl", "wb") as file:
                pickle.dump(nation_instance, file)
            print(f"Your game has been saved. Goodbye, {nation_instance.leader}.")
            game_continue = False
        elif response == "3":
            # Exit without saving
            print(f"Risky today, are we? Goodbye, {nation_instance.leader}.")
            game_continue = False
        else:
            print("Invalid choice. Please try again.")

def main():
    runtime(load_existing_save=False, existing_save_path=None)

if __name__ == '__main__':
    main()