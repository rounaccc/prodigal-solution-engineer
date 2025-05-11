import json
import os
import re
from collections import defaultdict
import yaml
import csv
import json
import yaml
from pathlib import Path
from groq import Groq
from tqdm import tqdm

def load_config(path='config.yaml'):
    with open(path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)
    
def load_profane_words(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def build_profanity_regex(profane_words):
    # Escape special characters and join into a regex pattern
    pattern = r'\b(?:' + '|'.join(re.escape(word.lower()) for word in profane_words) + r')\b'
    return re.compile(pattern, flags=re.IGNORECASE)

def detect_profanity(conversation, pattern):
    agent_count = 0
    customer_count = 0
    agent_words = []
    customer_words = []

    for utterance in conversation:
        speaker = utterance.get("speaker", "").lower()
        text = utterance.get("text", "").lower()

        matches = pattern.findall(text)

        if speaker == "agent":
            agent_count += len(matches)
            agent_words.extend(matches)
        elif speaker == "customer":
            customer_count += len(matches)
            customer_words.extend(matches)

    return {
        "agent": {
            "count": agent_count,
            "words": agent_words
        },
        "customer": {
            "count": customer_count,
            "words": customer_words
        }
    }


config = load_config()
config_paths = config['ProfaneWords']

# Initialize Groq Client
def get_groq_client():
    return Groq(api_key=config_paths['API_KEY'])

# Format conversation
def format_conversation(json_data):
    return "\n".join([f"{x['speaker']}: {x['text']}" for x in json_data])

# Profanity detection
# def check_profanity(convo_text, client, model="llama3-70b-8192"):
#     prompt = f"""Does this conversation contain any profanity or abusive language? 
# Give the answer strictly in the following Python list format:

# [
#   (True if Agent used any profane words else False),
#   (True if Customer used any profane words else False),
#   [List of profane words used by Agent, empty list if none],
#   [List of profane words used by Customer, empty list if none]
# ]

# Here is the conversation:
# {convo_text}
# """
#     try:
#         response = client.chat.completions.create(
#             messages=[{"role": "user", "content": prompt}],
#             model=model,
#         )
#         reply = response.choices[0].message.content.strip()
#         return eval(reply)
#     except Exception as e:
#         print("Error:", e)
#         return [False, False, [], []]

# Main processing function
# def process_all_to_dict(folder_path, client):
#     results = {}

#     for file in tqdm(Path(folder_path).glob("*.json")):
#         try:
#             with open(file, "r", encoding="utf-8") as f:
#                 convo_json = json.load(f)

#             convo_text = format_conversation(convo_json)
#             result = check_profanity(convo_text, client)

#             results[file.stem] = {
#                 "agent_profane": result[0],
#                 "customer_profane": result[1],
#                 "agent_words": result[2],
#                 "customer_words": result[3],
#                 "agent_word_count": len(result[2]),
#                 "customer_word_count": len(result[3])
#             }

#         except Exception as e:
#             print(f"Failed on {file.name}: {e}")

#     return results