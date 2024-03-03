from openai import OpenAI
import numpy as np
import json
import os
if os.path.exists('./secret.py'):
    from secret import openai_key
    print(openai_key)
from events import Event

json_chunk_length = 16 # Number of events in a JSON file

political_event_template = """
{
    "event_index": 0,
    "event_type": "political",
    "event_title": "The Great Cookie Conundrum",
    "event_description": "In the quirky nation of [Nation Name], a heated debate has erupted over the surprising discovery of an ancient law that requires all cookies sold in the country to be exactly 7.5 cm in diameter. This peculiar regulation, long forgotten in the annals of bureaucratic paperwork, came to light when a curious historian was rummaging through the national archives for material for their new book on odd laws. As news of this law spreads, cookie manufacturers are in turmoil, fearing the costs of adjusting their production lines, while purists argue for the preservation of tradition. The citizens are divided, with some seeing this as an opportunity to stand out in the global cookie market, while others view it as an unnecessary and costly imposition on businesses and consumers alike.",
    "event_options": [
        {
            "option_description": "It's time to embrace our cookie heritage! We should not only enforce this law but also create a national cookie inspection agency to ensure compliance. Our cookies will be famous worldwide for their precision and historical accuracy!",
            "option_outcome": "Cookie inspectors become the new celebrities, and the nation gains a quirky reputation as the home of the perfectly sized cookie.",
            "option_effects": {
                "political_freedom": 0.3,
                "economy": -0.4,
                "civil_rights": 0.0
            }
        },
        {
            "option_description": "Abolish this absurd law and let the market decide! If people want giant cookies or tiny cookies, who are we to stand in their way? Freedom in cookie size is the true path to economic prosperity.",
            "option_outcome":"The cookie market explodes with variety, leading to the rise of niche cookie startups specializing in all sizes, from micro-cookies to pizza-sized giants.",
            "option_effects": {
                "political_freedom": 0.6,
                "economy": 0.8,
                "civil_rights": -0.3
            }
        },
        {
            "option_description": "This is a perfect opportunity to lead the world in cookie-cutting technology. Let's invest in research and development to create adjustable cookie cutters for manufacturers. Make cookies of any size, but at the push of a button!",
            "option_outcome": "[Nation Name] becomes a hub for cookie technology innovation, attracting tech startups and leading to the unexpected side effect of a booming tech industry centered around food production.",
            "option_effects": {
                "political_freedom": 0.0,
                "economy": 0.9,
                "civil_rights": 0.4
            }
        },
        {
            "option_description": "We're missing the bigger picture. The real issue is the environmental impact of cookie production. Let's use this law to transition towards sustainable, organic cookie production that respects our planet.",
            "option_outcome": "The nation's cookies become a symbol of environmental sustainability, with the size regulation oddly contributing to a reduction in waste and an increase in green cookie manufacturing practices.",
            "option_effects": {
                "political_freedom": 0.7,
                "economy": -0.6,
                "civil_rights": 0.2
            }
        }
    ]
}
"""

political_event_prompt = """
I am developing an app that is similar to NationStates, the website where you create your own nation and make choices on political events that affect the nation's political, economic, and civil rights scores. I need you to help me create new events, responses to events, and their outcomes. This needs to be provided specifically in JSON format ONLY. Do not include any ancillary text outside of the JSON template. The JSON template is provided below. Do not change any of the key values. Do not alter event_type from "political". Do not use any reference to the nation other than [Nation Name]. Only replace the values with appropriate values for a new event. Emphasize randomness, humor, ridiculousness in the event, responses, and outcomes. 
"""

potential_topics = ["Taxation policies",
"Internet censorship",
"Environmental regulations",
"Space exploration",
"Public transportation",
"National holidays",
"Education reforms",
"Healthcare system",
"Artificial intelligence",
"Historical reenactments",
"Trade agreements",
"National anthems",
"Currency changes",
"Diplomatic relations",
"Election systems",
"Military parades",
"National sports teams",
"Food safety laws",
"Immigration policies",
"Wildlife conservation",
"Public housing",
"Renewable energy",
"Government transparency",
"Postal services",
"National dress codes",
"Public demonstrations",
"Privacy laws",
"Urban development",
"Virtual reality",
"Time zone adjustments",
"Cryptocurrency adoption",
"Universal basic income",
"Cultural heritage preservation",
"Pandemic response",
"Public art projects",
"National security laws",
"Voting rights",
"Nuclear energy policy",
"Foreign aid",
"Espionage and surveillance",
"Labor laws",
"Tourism industry",
"Public libraries",
"National parks",
"Disaster preparedness",
"Scientific research funding",
"Media ownership",
"Public celebrations",
"Traffic regulations",
"Animal rights",
"Water resource management",
"Outer space treaties",
"Sports betting",
"Youth engagement",
"Public speaking",
"National lottery",
"Cybersecurity measures",
"Historical monuments",
"National language",
"Public sector salaries",
"Fishing rights",
"International expositions",
"Climate change initiatives",
"Public pensions",
"Government scandals",
"Food festivals",
"National symbols",
"Gun control laws",
"Religious freedom",
"Government shutdowns",
"Waste management",
"Public safety",
"Trade tariffs",
"Intellectual property",
"Census taking",
"Alcohol regulations",
"Drone usage",
"Judicial reforms",
"Childcare policies",
"Public broadcasting",]

def generate_political_event(api_key:str=None):
    """
    Generates a new political event in JSON format.

    Args:
        api_key (str, optional): The API key for OpenAI. Defaults to None.

    Returns:
        str: The generated political event in JSON format.
    
    Raises:
        ValueError: If the API key is not provided.
    """
    if os.path.exists('secret.py'):
        api_key = openai_key
    elif api_key is not None:
        api_key = api_key
    if api_key is None:
        raise ValueError('API key not provided')
    client = OpenAI(api_key=api_key)
    current_topic = potential_topics[np.random.randint(0, len(potential_topics))]
    current_topic_text = f"You will be creating a new political event related to {current_topic}."
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role":"system","content":political_event_prompt + political_event_template + current_topic_text},
            {"role":"user","content":"I need a new event."},
        ],
        temperature=1,
        top_p=1,
        max_tokens=1024,
        response_format={"type":'json_object'},
        presence_penalty=0.0,
    )
    return response.choices[0].message.content

def json_to_file(json_string:str, filename:str):
    """
    Writes the given JSON string to a file.

    Args:
        json_string (str): The JSON string to write.
        filename (str): The name of the file to write to.
    """
    with open(filename, 'w') as f:
        f.write(json_string)

def political_event_generation_03_02_2024():
    """
    Generates and saves multiple political events.

    This function generates 50 political events using the `generate_political_event` function and saves them as JSON files.

    The generated events are saved in the '../event_storage' directory with filenames in the format 'political_event_{i}.json',
    where {i} is the index of the event.

    Note: This function assumes that the '../event_storage' directory already exists.
    """
    for i in range(10,60,1):
        val = generate_political_event()
        print(val)
        json_to_file(val, f'../event_storage/political_event_{i}.json')

def main():
    generate_political_event = True
    if generate_political_event:
        political_event_generation_03_02_2024()
    
if __name__ == '__main__':
    main()