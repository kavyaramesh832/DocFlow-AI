# 📄 DocuFlow AI

DocuFlow AI is a full-stack AI-powered system that automates the **ingestion, classification, and routing of documents**, with an intuitive dashboard for real-time tracking and analytics.

---

## 🚀 Demo Video
🎥 [Watch the demo here](https://your-video-link.com)

---

## 🔍 Features

- 📥 Drag-and-drop document upload
- 📧 Email ingestion (auto-fetches from Gmail)
- 🔍 OCR processing using Tesseract
- 🧠 Text preprocessing and ML-based classification
- 📂 Smart file routing to labeled folders
- 📊 Dashboard with real-time stats using Chart.js

---

## 🧠 Tech Stack

| Layer      | Technology           |
|------------|----------------------|
| Backend    | Flask (Python)       |
| OCR        | Tesseract            |
| ML         | scikit-learn, TF-IDF |
| Preprocess | NLTK, regex          |
| Frontend   | HTML, JS, Bootstrap  |
| Charts     | Chart.js             |
| Email      | IMAP, email module   |

---

## 🏗️ Architecture Overview

```mermaid
flowchart TD
    A[Upload Document / Email Fetch] --> B[OCR Extraction]
    B --> C[Text Preprocessing]
    C --> D[ML Classification]
    D --> E[File Routing]
    E --> F[Dashboard Update]
