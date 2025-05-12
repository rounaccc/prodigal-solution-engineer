# 🛡️ Conversation Metrics & Scrubbing Utility

### Technical Report: [Conversation Analysis Technical Report](https://github.com/user-attachments/files/20151092/Conversation.Analysis.Technical.Report.docx)

A modular pipeline to process conversation JSON files, analyze silence/overtalk durations, detect profane language, and detect sensitive information.

---

## 📁 Project Structure

```
.
├── artifacts/                       # Contains data, CSV documents, and intermediate outputs
├── research/                        # Jupyter notebooks used for staging and development
├── src/
│   └── utils/
│       ├── profane.py              # Utility functions for profanity detection
│       └── sensitive_information.py # Utility functions for redacting sensitive/PII info
├── app.py                           # Profanity and Sensitive Information Violation Streamlit
├── config.yaml                      # Contains file paths and API key configurations
├── main.py                          # Call Visualization Streamlit script
├── requirements.txt                 # Project dependencies
└── .gitignore
```

---

## 🚀 Features

- 📊 Silence & Overtalk Analysis
- 🤬 Profanity Detection
- 🔐 Sensitive Information Detection
- 📚 Jupyter Notebooks for research and staging

---

## Demo
- `app.py`

https://github.com/user-attachments/assets/b14a7668-0040-4c45-b1eb-dd8458623ad4

- `main.py`


https://github.com/user-attachments/assets/9e25e6ee-2a09-4ebf-b133-6d04e48ac366


## 🛠️ Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/rounaccc/prodigal-solution-engineer.git
cd your-repo-name
```

### 2. Set Up Virtual Environment (Optional but Recommended)

```bash
python -m venv .venv
source .venv/bin/activate        # On Windows: . .venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Your Setup

Update `config.yaml` with the appropriate API keys and paths.

---

## ✅ Usage

- `streamlit run app.py` - A Streamlit App for Profanity Detection and Sensitive Information Detection 
- `streamlit run main.py` - A Streamlit App for Conversation Duration Analysis
- Use individual utilities from `src/utils/`
- Explore and test features in `research/` notebooks

---


