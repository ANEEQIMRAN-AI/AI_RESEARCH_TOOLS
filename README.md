

# 🧠 Academic Writing Tools Suite

This repository contains four powerful AI-driven academic tools built using **LangChain**, **LangGraph**, **Google Gemini LLM**, and **Streamlit**. Each tool is designed to enhance writing, research, and productivity for students, researchers, and professionals.

---

## 📘 Contents

1. [🎓 Thesis Statement Generator](#-thesis-statement-generator)
2. [📝 AI Essay Writer](#-ai-essay-writer)
3. [✨ AI Paraphraser Agent (Standard)](#-ai-paraphraser-agent-standard)
4. [✍️ AI Paraphraser Agent (Enhanced Version)](#-ai-paraphraser-agent-enhanced-version)

---

# 🎓 Thesis Statement Generator

This project is a **Thesis Statement Generator** built with **Streamlit**, **LangChain**, **LangGraph**, and **Google Gemini LLM**. It helps generate polished, academic-quality thesis statements based on user input, while also fetching related research articles.

## 🚀 Features

* **Structured Thesis Generation:** Produces 10 diverse, structured, and arguable thesis statements.
* **Humanization:** Refines generated statements to sound fluent, natural, and academic.
* **Grammar Checking:** Reviews and corrects grammar, clarity, and fluency.
* **Related Articles Search:** Fetches recent related research articles from trusted academic sources.
* **Streamlit UI:** Interactive interface with input fields and result display.

## 🛠️ Technologies Used

* **Python**
* **Streamlit**
* **LangChain / LangGraph**
* **Google Gemini LLM (via API)**
* **Google Custom Search API**

## 📦 Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/thesis-generator.git
   cd thesis-generator
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**

   Create a `.env` file in the root directory and add:

   ```bash
   GOOGLE_API_KEY=your_google_gemini_api_key
   GOOGLE_SEARCH_API_KEY=your_google_custom_search_api_key
   GOOGLE_CSE_ID=your_google_custom_search_engine_id
   ```

   * Get `GOOGLE_API_KEY` from your Google Gemini API credentials.
   * Enable [Custom Search API](https://console.cloud.google.com/apis/library/customsearch.googleapis.com) and create credentials to obtain `GOOGLE_SEARCH_API_KEY` and `GOOGLE_CSE_ID`.

## ▶️ Usage

Run the app using Streamlit:

```bash
streamlit run thesis_agent_generator.py
```

## 🎯 How It Works

* Enter your thesis topic, along with optional main idea, supporting reasons, and intended audience.
* Click **Generate** to get 10 structured, polished thesis statements.
* See related research articles fetched using Google Custom Search.

## ✅ TODO / Future Improvements

* Add citation formatting in MLA / APA style.
* Export thesis statements to PDF or Word.
* Integrate plagiarism checking.

## 📄 License

MIT License. See `LICENSE` file for details.


---

# 📝 AI Essay Writer

This project is an **AI Essay Writing Agent** that generates high-quality academic essays using **LangChain**, **LangGraph**, **Google Gemini LLM**, and **Streamlit**. It ensures the final output is well-written, humanized, grammatically correct, and plagiarism-safe.

## 🚀 Features

* **Full Essay Generation:** Write complete academic essays on any topic.
* **Natural Tone & Flow:** Outputs sound fluent and professional.
* **PhD-Level Structure:** Essays follow academic standards with intro, body, and conclusion.
* **Streamlit UI:** Clean and interactive user interface for input and output display.

## 🛠️ Technologies Used

* **Python**
* **LangChain / LangGraph**
* **Google Gemini LLM**
* **Streamlit**

## 📦 Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/ai-essay-writer.git
   cd ai-essay-writer
   ```

2. **Create and activate virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install requirements:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Environment variables:**

   Create a `.env` file and add:

   ```env
   GOOGLE_API_KEY=your_google_gemini_api_key
   ```

## ▶️ Usage

Run using Streamlit:

```bash
streamlit run AI_ESSAY.py
```

## 📄 Essay Structure

Each essay follows this structure:

* **Introduction:** Hook, background, thesis, roadmap
* **Body Paragraphs:** Topic sentence, evidence, analysis, transitions
* **Conclusion:** Summary, synthesis, implications, lasting impression

## ✅ TODO / Future Enhancements

* Add citation integration (APA/MLA)
* PDF export option
* Add tone and length control
* Add plagiarism percentage feedback

## 📄 License

MIT License. See `LICENSE` file for details.


---

# ✨ AI Paraphraser Agent (Standard)

This project is an **AI-based Paraphrasing Tool** built with **LangChain**, **LangGraph**, **Streamlit**, and **Google Gemini LLM**. It takes any paragraph or PDF content as input and intelligently rephrases, humanizes, and grammatically corrects it for natural and fluent output.

## 🚀 Features

* **Professional Rephrasing:** Rewrites content while preserving its original meaning and avoiding redundancy or plagiarism.
* **Extreme Humanization:** Enhances fluency and makes text sound like it was written by a native speaker.
* **Grammar Correction:** Fixes all grammatical, punctuation, and structural issues.
* **PDF Input Support:** Automatically extracts and processes text from uploaded PDFs.
* **Word Count:** Displays real-time word count of input and output text.
* **Streamlit UI:** Intuitive interface with input box, buttons, and output panel.

## 🛠️ Technologies Used

* **Python**
* **Streamlit**
* **LangChain / LangGraph**
* **Google Gemini LLM (via API)**
* **PyPDF2**

## 📦 Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/paraphraser-agent.git
   cd paraphraser-agent
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**

   Create a `.env` file in the root directory and add:

   ```env
   GOOGLE_API_KEY=your_google_gemini_api_key
   ```

## ▶️ Usage

Run the app using Streamlit:

```bash
streamlit run AI_PARAPHRASER.py
```

## 🧠 How It Works

* Enter a paragraph or upload a PDF.
* Click "Paraphrase" to get a rewritten, humanized, grammatically correct output.
* View real-time word count for both input and output.

## ✅ TODO / Future Enhancements

* Add language and tone selection (e.g., formal, academic, conversational)
* Export final output as PDF or DOCX
* Add plagiarism checker integration
* Support DOCX file uploads

## 📄 License

MIT License. See `LICENSE` file for details.


---

# ✍️ AI Paraphraser Agent (Enhanced Version)

This project is a **Paraphrasing AI Agent** built using **LangChain**, **LangGraph**, and **Google Gemini LLM**, with a smooth **Streamlit UI**. It takes your input paragraph and transforms it into a fully humanized, grammatically flawless, and plagiarism-safe version.

## 🚀 Features

* **Deep Paraphrasing:** Rewrites input text using advanced vocabulary and sentence structure while preserving original meaning.
* **Humanization:** Makes the paraphrased output sound natural, emotionally resonant, and free from robotic tone.
* **Grammar Correction:** Detects and fixes all grammar, punctuation, and syntax issues.
* **Plagiarism Elimination:** Deeply rewrites the final output to ensure near 0% plagiarism.
* **Streamlit UI:** Simple and interactive web interface for easy use.

## 🛠️ Technologies Used

* **Python**
* **LangChain** & **LangGraph**
* **Google Gemini LLM (via API)**
* **Streamlit**

## 📦 Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/paraphraser-agent.git
   cd paraphraser-agent
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install the dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**

   Create a `.env` file and add:

   ```env
   GOOGLE_API_KEY=your_google_gemini_api_key
   ```

## ▶️ Usage

Run the app via Streamlit:

```bash
streamlit run app.py
```

## 📄 Output Quality

* Fully rewritten, plagiarism-safe paragraphs
* Academic-level vocabulary and grammar
* Human-style tone and clarity
* Natural transitions and narrative flow

## ✅ TODO / Future Enhancements

* Add multilingual support
* Provide downloadable reports (Word/PDF)
* Integrate plagiarism percentage checker
* Export to Google Docs

## 📄 License

MIT License. See `LICENSE` file for details.

---
