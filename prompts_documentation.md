# AI Prompt Documentation
## Health Prediction App – Gokul Infocare Task 2

### 1. Project Overview

The Health Prediction App is a Python-based patient information management application developed using Streamlit, SQLite, and Google's Gemini API.

The application uses Generative AI to provide educational explanations of patient blood test values, including glucose, haemoglobin, and cholesterol.

### 2. AI Model and API

- **AI Provider:** Google Gemini
- **Model:** gemini-3.8-flash
- **Python SDK:** google-genai
- **Integration:** Gemini API using the `google-genai` Python package
- **API Key Management:** Environment variable loaded using `python-dotenv`

### 3. Purpose of the AI Prompt

The AI prompt is designed to:
- Explain the three blood test values.
- Describe potential health concerns cautiously.
- Avoid making medical diagnoses.
- Explain the importance of laboratory units and reference ranges.
- Recommend consultation with qualified healthcare professionals.
- Provide a medical disclaimer.

### 4. Main AI Prompt

The following prompt is sent to the Gemini API:

```text
You are an AI health information assistant.

Review these blood test values:
Glucose: {glucose}
Haemoglobin: {haemoglobin}
Cholesterol: {cholesterol}

Instructions:
- Do not assume measurement units.
- Do not assume whether glucose was fasting or random.
- Explain that interpretation depends on units and lab reference ranges.
- Do not diagnose any disease.
- Give cautious, understandable health information.
- Recommend professional medical review.
- Include a medical disclaimer.

Format:
1. Blood Test Value Explanation
2. Potential Health Concerns
3. Recommendations
4. Disclaimer
```

### 5. Input Parameters

The application dynamically passes the following values to the AI model:

| Parameter | Description |
|---|---|
| Glucose | Patient's glucose test value |
| Haemoglobin | Patient's haemoglobin test value |
| Cholesterol | Patient's cholesterol test value |

The values are taken from the patient form or database record.

### 6. AI Response Processing

1. The application receives patient blood test values.
2. The values are inserted into the AI prompt.
3. The Gemini API processes the prompt.
4. The generated explanation is returned to the application.
5. The AI-generated remarks are stored in the SQLite database.
6. The remarks are displayed in the patient record.

### 7. Error Handling

The application handles situations such as:

- Missing Gemini API key.
- API connection or service errors.
- Empty AI responses.

When the AI service is unavailable, an informative fallback message is returned so patient record management can continue.

### 8. Safety and Limitations

- AI-generated remarks are informational and educational only.
- The application does not provide a confirmed medical diagnosis.
- Clinical interpretation requires laboratory units, reference ranges, and patient context.
- Users should consult qualified healthcare professionals for medical advice.
- The application is not a substitute for clinical evaluation or treatment.

### 9. Security

The Gemini API key is stored in a local `.env` file and loaded through environment variables.

The `.env` file is excluded from GitHub using `.gitignore`.

### 10. Conclusion

The Gemini API integration demonstrates how Generative AI can be used to produce understandable explanations of health-related laboratory values within a patient management application.

**Project:** AI Health Information System  
**Developer:** Preeti Tavag  
**Assessment:** Gokul Infocare – AI Growth & Automation Associate, Task 2