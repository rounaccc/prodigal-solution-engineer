import re
import json
from pathlib import Path
from tqdm import tqdm

def get_sensitive_patterns():
    return {
        "ssn": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
        "phone": re.compile(r"\b(?:\+91[-\s]?|0)?\d{10}\b"),
        "email": re.compile(r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}\b"),
        "credit_card": re.compile(r"\b(?:\d{4}[-\s]?){3}\d{4}\b"),
        "address": re.compile(r"\b\d{1,5}\s\w+\s(?:Street|St|Avenue|Ave|Road|Rd|Lane|Ln)\b", re.I),
        "pan": re.compile(r"\b[A-Z]{5}\d{4}[A-Z]\b"),
        "aadhaar": re.compile(r"\b\d{4}\s\d{4}\s\d{4}\b"),
        "phone": re.compile(r"\b\d{3}-\d{3}-\d{4}\b"),
        "address": re.compile(r'\d+\s\w+\s\w+,\s\w+'),
        "passport": re.compile(r"\b[A-Z]{1}[0-9]{7}\b"),
        "bank_account": re.compile(r"\b\d{9,18}\b"),
        "dob": re.compile(r"\b\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\b")
    }

def get_verification_keywords():
    return ["date of birth", "dob", "address", "ssn", "social security number", "verification"]

def contains_verification(text):
    text = text.lower()
    return any(key in text for key in get_verification_keywords())

def contains_sensitive(text, patterns):
    found = []
    for name, pattern in patterns.items():
        if pattern.search(text):
            found.append(name)
    return found

def check_privacy_violation(convo_json):
    patterns = get_sensitive_patterns()
    verified = False
    violations = []

    for line in convo_json:
        speaker = line["speaker"]
        text = line["text"]

        if speaker.lower() == "agent":
            if contains_verification(text):
                verified = True

            if not verified:
                sensitive_found = contains_sensitive(text, patterns)
                if sensitive_found:
                    violations.extend(sensitive_found)
        verified = False  # Reset for the next line

    return list(set(violations))  # Unique violation types

