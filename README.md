# 🏥 AI Health Information System

An AI-powered patient health information management application built using Python, Streamlit, SQLite, and Google's Gemini API.

The application allows users to manage patient records, validate health information, and generate AI-assisted explanations of blood test values.

## 🚀 Features

- **Patient Management:** Add, view, edit, and delete patient records.
- **Input Validation:** Validate email addresses, dates of birth, and numeric health values.
- **Bulk Data Import:** Import and validate the 10 assessment test records.
- **AI-Generated Remarks:** Use Google's Gemini API to generate explanations of glucose, haemoglobin, and cholesterol values.
- **Database Storage:** Store patient information persistently using SQLite.
- **CSV Export:** Download patient records as a CSV file.
- **Duplicate Records:** Preserve legitimate duplicate patient entries as separate records.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Streamlit | User interface |
| SQLite | Database management |
| Google Gemini API | AI-generated health remarks |
| Pandas | Data handling and CSV export |
| Python-dotenv | Environment variable management |

## 📁 Project Structure

```text
HealthPredictionApp/
│
├── app.py
├── database.py
├── validation.py
├── ai_health.py
├── requirements.txt
├── README.md
├── .gitignore
└── .env                 # Local only; not uploaded
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/preetitavag28/HealthPredictionApp.git
```

### 2. Navigate to the project folder

```bash
cd HealthPredictionApp
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure the Gemini API key

Create a `.env` file in the project root directory:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Replace the placeholder with your own API key.

Get an API key from [Google AI Studio](https://aistudio.google.com/apikey).

**Security:** Never upload your `.env` file or expose your API key publicly.

### 7. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

## 🧪 Assessment Test Data

The application supports importing 10 supplied patient records.

- Valid records are saved to the SQLite database.
- Invalid email addresses are rejected.
- Impossible and future dates of birth are rejected.
- Duplicate patient records are retained.
- Validation results are displayed in a report.

## 🤖 AI Integration

The application integrates Google's Gemini API to generate educational explanations of:

- Blood glucose values
- Haemoglobin values
- Cholesterol values

The generated remarks explain that interpretation depends on laboratory units, reference ranges, and clinical context.

## 🩺 Medical Disclaimer

This application is intended for educational and informational purposes only. AI-generated remarks are not medical diagnoses and must not replace professional medical advice, clinical evaluation, or treatment.

## 👩‍💻 Developer

**Preeti Tavag**

MCA Graduate | Software Developer

- GitHub: [preetitavag28](https://github.com/preetitavag28)
- Email: preetitavag@gmail.com

---

*Developed as part of the AI Growth & Automation Associate – Task 2 assessment.*
