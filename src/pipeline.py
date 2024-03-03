from nation import Nation
from events import Event, event_from_json
from event_generation import json_chunk_length
import numpy as np
import os
import json
import pickle
import argparse

def event_loop(nation_instance, event_type="political"):
    """
    Runs the event loop for the given nation instance.

    Args:
        nation_instance (Nation): The instance of the nation.
        event_type (str, optional): The type of events to process. Defaults to "political".

    Returns:
        Nation: The updated nation instance after processing the events.
    """
    if event_type != "political":
        raise NotImplementedError("Only political events are supported at this time.")
    encountered_events = nation_instance.encountered_events
    total_events = len(os.listdir("../event_storage"))
    # Choose a random event that the user hasn't encountered yet
    event_index = np.random.randint(0, total_events)
    while event_index in encountered_events:
        event_index = np.random.randint(0, total_events)
    match event_type:
        case "political":
            filename = f"../event_storage/political_event_{event_index}.json"
        case "economic":
            raise NotImplementedError("Only political events are supported at this time.")
        case "military":
            raise NotImplementedError("Only political events are supported at this time.")
    
    event = event_from_json(filename) # Load event from file
    response = event.respond_to_event(nation_instance) # Get user response
    nation_instance.encountered_events.add(event_index) # Make sure that the user doesn't get the same event again
    
    return nation_instance

def runtime(load_existing_save=False, existing_save_path=None):
    """
    Runs the game loop for the Conquest game.

    Args:
        load_existing_save (bool, optional): Whether to load an existing save file. Defaults to False.
        existing_save_path (str, optional): The path to the existing save file. Required if load_existing_save is True.

    Returns:
        None
    """
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
            nation_instance = event_loop(nation_instance)
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
            print("Invalid choice. Please enter the number corresponding to your desired action.")

def main():
    runtime(load_existing_save=False, existing_save_path=None)

if __name__ == '__main__':
    main()