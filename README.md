# 📖 Quran & Hadith Search Engine

A search engine for Quran and Hadith that allows users to search for specific Surahs, Ayahs, translations, and Tafseer, as well as Hadith references based on different collections.

## 🚀 Features
- Search by **Surah & Ayah number** (e.g., `2:43`)
- Get **translations & Tafseer** for Quranic verses
- Search Hadith collections by **Hadith number, topic, or keywords**
- Support for **multi-language** responses

*Note: Some Hadith data may be incomplete.*

🔗 This project requires API access from:
- Groq → [Get API Key](https://console.groq.com/docs/quickstart)
- Gemini AI → [Get API Key](https://aistudio.google.com/)

---

## 🛠 Installation

### Clone the Repository
```bash
git clone https://github.com/fahmiaziz98/ramadhan2025.git
cd ramadhan2025
```

### Create & Activate Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate    # On Windows
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

---
## Create a Qdrant Cluster
- Sign up and create a Qdrant cluster to store and retrieve vectorized Hadith data.
- Get your API key and URL from [Qdrant docs](https://qdrant.tech/documentation/cloud/create-cluster/).
---

## 🐳 Docker Setup

### Build the Docker Image
```bash
cd backend/quran
docker build -t quran-api .
```

**Run the Container**
```bash
docker run -p 7860:7860 quran-api
```

For Hadith API, run the same command in the `backend/hadith` directory. The API will be available at http://localhost:7860/docs.

---

## Running the App with Streamlit
```bash
streamlit run app.py
```


Then, open your browser and go to **http://localhost:8501**.

---

## Recommended Deployment (Free)
- You can deploy the Quran & Hadith API for free using Hugging Face Spaces.
- Follow this [guide](https://huggingface.co/blog/HemanthSai7/deploy-applications-on-huggingface-spaces) to deploy your application.
