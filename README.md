# 📊 Analyst AI: Earnings Analyzer

**Analyst AI** is a financial analysis tool powered by **Google Gemini 1.5 Flash**. It ingests earnings reports (including scanned PDFs/images), performs server-side OCR, and extracts structured insights, sentiment analysis, and forward guidance into an interactive dashboard.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-8E75B2?style=for-the-badge&logo=google&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white)

## 🚀 Key Features

* **📄 AI-Powered OCR:** Directly processes scanned PDFs and images without needing external OCR libraries (Tesseract, etc.).
* **🧠 Financial Sentiment Analysis:** Detects management tone (Optimistic/Cautious) and assigns a confidence score.
* **🔍 Strategic Extraction:** Automatically pulls:
    * **Key Takeaways:** Bullish (Positives) and Bearish (Concerns) factors.
    * **Guidance:** Revenue, Margin, and Capex outlooks.
    * **Operational Updates:** Capacity utilization and new growth initiatives.
* **📊 Interactive Dashboard:** Presents complex JSON data in clean, readable tiles using Streamlit.

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/yourusername/analyst-ai.git](https://github.com/yourusername/analyst-ai.git)
cd analyst-ai
2. Create a Virtual Environment (Optional but Recommended)
Bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
3. Install Dependencies
Bash
pip install -r requirements.txt
Note: If you don't have a requirements.txt, create one with the following content:

Plaintext
streamlit
google-generativeai
🏃‍♂️ Running the App
Start the Streamlit server:

Bash
streamlit run app.py
The app will open in your browser at http://localhost:8501.

🔑 Configuration
To use the app, you need a Google Gemini API Key.

Get a free key here: Google AI Studio

Enter the key in the application sidebar.

(Optional): To avoid entering the key every time locally, create a .streamlit/secrets.toml file:

Ini, TOML
# .streamlit/secrets.toml
GEMINI_API_KEY = "your-api-key-here"
📸 Screenshots
Upload Interface	Analysis Dashboard
(Add a screenshot of your upload page here)	(Add a screenshot of your results page here)
🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

Fork the project

Create your Feature Branch (git checkout -b feature/AmazingFeature)

Commit your Changes (git commit -m 'Add some AmazingFeature')

Push to the Branch (git push origin feature/AmazingFeature)

Open a Pull Request

⚠️ Disclaimer
This tool is for informational purposes only. The analysis provided by the AI model may contain inaccuracies or hallucinations. It should not be considered professional financial advice. Always verify data against the official source documents.

Made with ❤️ using Streamlit and Google Gemini.
