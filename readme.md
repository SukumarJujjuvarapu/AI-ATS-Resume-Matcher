# 🚀 Smart ATS Resume Matcher

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-FF4B4B)
![AI Model](https://img.shields.io/badge/AI-Llama--3-orange)
![Status](https://img.shields.io/badge/Status-Active-success)

**A cutting-edge AI-powered Application Tracking System (ATS) that helps job seekers optimize their resumes using Large Language Models (LLMs).**

This tool mimics the experience of a real ATS used by Fortune 500 companies. It analyzes your resume against a job description (JD) to provide a **match percentage**, **missing keywords**, and a **strategic improvement plan**.

---

## 📸 Screenshots

![Dashboard Preview](https://via.placeholder.com/800x400?text=Your+App+Screenshot+Here)
*(Replace this link with a screenshot of your actual running app)*

---

## 🧠 Key Features

- **✅ Deep Gap Analysis:** Uses `Llama-3` (via Groq) to understand the *context* of skills, not just keyword matching.
- **📊 Smart Scoring:** Provides a match percentage based on semantic relevance.
- **🕵️ Missing Keywords:** Identifies critical skills missing from your resume that the JD demands.
- **💡 Strategic Advice:** Offers actionable tips to improve your profile (e.g., "Add a project about X").
- **📄 PDF Support:** Built-in PDF parsing to extract text from real-world resumes.

---

## 🛠️ Tech Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Frontend** | [Streamlit](https://streamlit.io/) | Interactive web-based user interface |
| **LLM Engine** | [Groq API](https://groq.com/) | Ultra-fast inference using **Llama-3-70b** |
| **Backend** | Python | Core application logic |
| **PDF Processing** | PyPDF2 | Extracts text from PDF documents |

---

## ⚙️ Installation & Setup

Follow these steps to run the project locally on your machine.

### 1. Clone the Repository
```bash
git clone [https://github.com/SukumarJujjuvarapu/Resume-AI-Matcher.git](https://github.com/SukumarJujjuvarapu/Resume-AI-Matcher.git)
cd Resume-AI-Matcher

Create a Virtual Environment (Optional but Recommended)
Bash

python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate


Install Dependencies
Bash

pip install -r requirements.txt


Configure API Keys
Create a file named .env in the root directory (or use Streamlit secrets) and add your Groq API key:

Ini, TOML

GROQ_API_KEY=gsk_your_actual_api_key_here


Run the Application
Bash

streamlit run app.py


🚀 How It Works
Upload Resume: The user uploads a PDF version of their resume.

Paste JD: The user copies the Job Description from LinkedIn/Indeed.

AI Analysis: The app sends both texts to the Groq Llama-3 model with a custom prompt engineered to act as a generic HR Manager.

Result: The AI returns a structured JSON response containing the score, missing skills, and formatting advice, which is parsed and displayed on the dashboard.


📂 Project Structure
Plaintext

Resume-AI-Matcher/
├── app.py                # Main Streamlit application
├── requirements.txt      # List of dependencies
├── .env                  # API Key storage (GitIgnored)
└── README.md             # Project documentation


🤝 Contributing
Contributions are welcome! Please follow these steps:

Fork the repository.

Create a new branch (git checkout -b feature-branch).

Commit your changes.

Push to the branch and open a Pull Request.
