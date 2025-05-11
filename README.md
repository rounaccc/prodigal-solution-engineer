# 🛡️ Conversation Metrics & Scrubbing Utility

A modular pipeline to process conversation JSON files, analyze silence/overtalk durations, detect profane language, and scrub sensitive information (like PII).

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
├── app.py                           # Entry point for web/app interface (Streamlit/Flask)
├── config.yaml                      # Contains file paths and API key configurations
├── main.py                          # Main script to run the pipeline
├── requirements.txt                 # Project dependencies
└── .gitignore
```

---

## 🚀 Features

- 📊 Silence & Overtalk Analysis
- 🤬 Profanity Detection
- 🔐 Sensitive Information Redaction
- 📚 Jupyter Notebooks for research and staging

---

## 🛠️ Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 2. Set Up Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Your Setup

Update `config.yaml` with the appropriate API keys and paths.

---

## ✅ Usage

You can either:

- Run the entire pipeline using `main.py`
- Use individual utilities from `src/utils/`
- Explore and test features in `research/` notebooks
- Launch the app via `app.py` (if integrated with Streamlit/Flask)

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

---

## 📄 License

This project is licensed under the MIT License.
