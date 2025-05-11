import streamlit as st
import pandas as pd
import os
import tempfile
import json
from src.utils.profane import load_config, load_profane_words, build_profanity_regex, detect_profanity, get_groq_client, format_conversation
from src.utils.sensitive_information import get_sensitive_patterns, contains_verification, contains_sensitive, check_privacy_violation

def profane_regex_implementation(files, profane_words):
    pattern = build_profanity_regex(profane_words)
    results = []

    for uploaded_file in files:
        try:
            convo = json.load(uploaded_file)
            file_id = os.path.splitext(uploaded_file.name)[0]
            result = detect_profanity(convo, pattern)

            results.append({
                "Call ID": file_id,
                "Agent Profane": result["agent"]["count"] > 0,
                "Customer Profane": result["customer"]["count"] > 0,
                "Agent Profane Count": result["agent"]["count"],
                "Customer Profane Count": result["customer"]["count"],
                "Agent Profane Words": ', '.join(result["agent"]["words"]),
                "Customer Profane Words": ', '.join(result["customer"]["words"])
            })
        except Exception as e:
            st.error(f"Failed to process {uploaded_file.name}: {e}")
    return results

import ast

def profane_llm_implementation(uploaded_files, client, model="llama3-70b-8192"):
    results = []

    for uploaded_file in uploaded_files:
        try:
            # Read JSON content
            convo = json.load(uploaded_file)
            convo_formatted = format_conversation(convo)

            prompt = f"""Does this conversation contain any profanity or abusive language? 
                    Give the answer strictly in the following Python list format:

                    [
                    (True if Agent used any profane words else False),
                    (True if Customer used any profane words else False),
                    [List of profane words used by Agent, empty list if none],
                    [List of profane words used by Customer, empty list if none]
                    ]

                    # Note: The answer should be in the format of a Python list, No extra text or explanation is needed.
                    # Example Output: [True, False, ['damn', 'hell'], []]
                    # Example Output: [False, True, [], ['idiot', 'stupid']]

                    Here is the conversation:
                    {convo_formatted}"""

            response = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=model,
            )

            raw_reply = response.choices[0].message.content.strip()
            print(f"Raw Reply for {uploaded_file.name}: {raw_reply}")

            # Safe parsing
            reply = ast.literal_eval(raw_reply)

            # Validate response format
            if not (isinstance(reply, list) and len(reply) == 4):
                raise ValueError("Malformed response format")

            results.append({
                "Call ID": uploaded_file.name.split('.')[0],
                "Agent Profane": reply[0],
                "Customer Profane": reply[1],
                "Agent Profane Words": ", ".join(reply[2]),
                "Customer Profane Words": ", ".join(reply[3]),
                "Agent Profane Count": len(reply[2]),
                "Customer Profane Count": len(reply[3])
            })

        except Exception as e:
            print(f"❌ Error processing {uploaded_file.name}: {e}")
            continue

    return results


def sensitive_information_regex_implementation(file):
    try:
        convo = json.load(file)
        file_id = os.path.splitext(file.name)[0]
        patterns = get_sensitive_patterns()
        violations = check_privacy_violation(convo)

        return {
            "Call ID": file_id,
            "Sensitive Information Violations": violations
        }
    except Exception as e:
        st.error(f"Failed to process {file.name}: {e}")
        return None

def sensitive_information_llm_implementation(uploaded_files, client, model="llama3-70b-8192"):
    results = []

    for uploaded_file in uploaded_files:
        try:
            convo = json.load(uploaded_file)
            convo_formatted = format_conversation(convo)

            prompt = f"""
            I am giving you a conversation between a customer and an agent in JSON format.
            Check if agent has shared any sensitive information with the customer without verification of customer.
            Sensitive information includes:
            1. Account balance of customer
            2. Account details of customer
            3. Acount number of customer

            Verificationinformation includes:
            1. Date of birth
            2. Address
            3. Social Security Number
            4. Any other information that can be used to identify the customer

            Strictly give output in this Python list format:

            [True if shared else False] 

            NOTE: I do not want python code. I do not want any explanation.
            Example Agent : "Your balance is $500.00"
            Example: [True] or [False]

            Here is the conversation between the customer and agent in JSON format:
            {convo_formatted}
            """

            response = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=model,
            )

            reply = response.choices[0].message.content.strip()
            reply = eval(reply)

            results.append({
                "Call ID": uploaded_file.name.split('.')[0],
                "Sensitive Information Violation": reply[0]
            })

        except Exception as e:
            print(f"Error processing {uploaded_file.name}: {e}")
            continue

    return results



def main():
    # results = []
    st.set_page_config(page_title="Conversation Analysis", layout="wide")
    st.title("🧼 Call Conversation Analysis - Prodigal")

    st.subheader("Choose Analysis Method")
    method = st.selectbox("Select Profanity Detection Method:", ["Regex", "LLM"])

    st.subheader("Choose Use Case")
    use_case = st.selectbox("Select Profanity Detection Method:", ["Identify Profanity", "Sensitive Information Violation"])

    uploaded_files = st.file_uploader(
        "Upload JSON files (multiple conversations allowed)", 
        type="json",
        accept_multiple_files=True
    )

    results = []

    if uploaded_files:
        config = load_config()
        profane_words = load_profane_words(config['ProfaneWords']['PROFANE_WORDS_PATH'])

        st.info("Analyzing uploaded conversations...")

        if method == "Regex" and use_case == "Identify Profanity":
            results = profane_regex_implementation(uploaded_files, profane_words)

        elif method == "LLM" and use_case == "Identify Profanity":
            client = get_groq_client()
            results = profane_llm_implementation(uploaded_files, client)

        elif method == "Regex" and use_case == "Sensitive Information Violation":
            results = []
            for uploaded_file in uploaded_files:
                result = sensitive_information_regex_implementation(uploaded_file)
                if result:
                    results.append(result)

        elif method == "LLM" and use_case == "Sensitive Information Violation":
            client = get_groq_client()
            results = sensitive_information_llm_implementation(uploaded_files, client)

        if results:
            df = pd.DataFrame(results)
            st.success(f"✅ Processed {len(results)} conversations using {method}.")
            st.dataframe(df, use_container_width=True)

            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name="Call_Summary.csv",
                mime="text/csv"
            )
        else:
            st.warning("No valid conversation data was processed.")

if __name__ == "__main__":
    main()
