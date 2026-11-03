# 🌐 Language Translation Tool

An attractive, modern, and responsive **Language Translation Tool** built with **Python (Flask)** on the backend and **HTML5, CSS3, and JavaScript** on the frontend. Developed as part of the **CodeAlpha Artificial Intelligence Internship**.




LIVE DEMO : https://code-alpha-language-translation-too-beryl.vercel.app/
---

## 📌 Project Overview

This project provides an intuitive web-based interface that enables users to translate text between **70+ world languages** seamlessly. Powered by modern Neural Machine Translation (NMT), the tool delivers accurate and natural translations without requiring paid API keys or complicated setups.

---

## ✨ Features

- **🌐 70+ Supported Languages**: Translate text to and from over 70 languages including English, Spanish, French, German, Hindi, Arabic, Chinese, Japanese, and more.
- **🔍 Auto Language Detection**: Automatically detects the source language when set to *Auto Detect*.
- **⇄ Swap Languages**: Easily swap between source and target languages and text box contents with one click.
- **📋 Copy to Clipboard**: Dedicated copy button with instant feedback to copy translated results.
- **🗑 Clear / Reset**: One-click reset for inputs, translations, and character counters.
- **📊 Live Character Counter**: Keeps track of typed characters in real time (up to 5,000 characters).
- **⚡ Keyboard Shortcuts**: Press `Ctrl + Enter` (or `Cmd + Enter`) to translate instantly from the keyboard.
- **⏳ Loading State**: Clear visual spinner indicator while translations are processing.
- **📱 Fully Responsive Design**: Adapts cleanly across desktop monitors, tablets, and mobile devices.
- **🛡️ Resilient Multi-Engine Fallback**: Built with high availability in mind; falls back across neural engines to prevent rate-limiting and timeouts.

---

## 🛠️ Tech Stack

- **Backend**: Python 3, Flask
- **Translation Engine**: Neural Machine Translation (NMT) via `translators` (Microsoft Bing / Multi-engine fallback)
- **Frontend**: HTML5, CSS3 (Custom animations & gradient styling), Vanilla JavaScript (ES6+ Fetch API, Clipboard API)

---

## 📁 Project Structure

```text
Language_Translator/
│
├── app.py                 # Flask server, routing, and translation engine
├── requirements.txt       # Project dependencies
├── .gitignore             # Files to exclude from version control
├── README.md              # Project documentation
│
├── templates/
│   └── index.html         # Main application web page
│
└── static/
    ├── style.css          # Gradient background, responsive grid & animations
    └── script.js          # Asynchronous translation, swap, copy, and clear logic
```

---

## 🚀 Getting Started

Follow these steps to run the project locally on your machine.

### 1. Clone the Repository
```bash
git clone https://github.com/Dishal-05/CodeAlpha_Language_Translation_Tool.git
cd CodeAlpha_Language_Translation_Tool
```

### 2. Create a Virtual Environment (Optional but Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
python app.py
```

### 5. Open in Your Browser
Visit: **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 💡 Usage Guide

1. Enter or paste text into the **Original Text** box.
2. Select the **Source Language** (or leave it on *Auto Detect*).
3. Select your desired **Target Language**.
4. Click **🔤 Translate** (or press `Ctrl + Enter`).
5. Use **📋 Copy Translation** to copy the result, or **⇄** to swap languages.

---

## 👨‍💻 Author

- **GitHub**: [@Dishal-05](https://github.com/Dishal-05)
- **Internship**: CodeAlpha Artificial Intelligence Internship

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
