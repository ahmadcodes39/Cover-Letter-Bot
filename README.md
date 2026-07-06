# Cover Letter & Cold Email Tailor Bot

A small Chatbot that uses Google Gemini to turn a job description and a candidate summary into a tailored cover letter or cold email.

## Features

- Paste a job description and your background summary.
- Generate either a cover letter or a cold email.
- Refine the draft with follow-up prompts such as "make it shorter" or "more formal".
- Handles common API issues like quota, rate limits, and safety blocks with user-friendly messages.

## Project Structure

- `app.py` - Streamlit application entry point.
- `requirements.txt` - Python dependencies.

## Prerequisites

- Python 3.10 or newer.
- A Google Gemini API key.

## Setup

1. Create and activate a virtual environment.
2. Install the dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root and add your API key:

```env
GEMINI_API_KEY=your_api_key_here
```

## Run the App

Start the Streamlit app with:

```bash
streamlit run app.py
```

Then open the local URL shown in the terminal, usually `http://localhost:8501`.

## How to Use

1. Paste the job description into the first text box.
2. Paste your CV summary or key skills into the second text box.
3. Choose whether you want a cold email or a cover letter.
4. Click Generate.
5. Use the follow-up chat box to ask for edits or tone changes.

## Notes

- Keep the job description under 8,000 characters.
- Keep the background summary under 4,000 characters.
- If you see a quota or rate-limit message, wait and try again later.

## Troubleshooting

- If the app says the API key is missing, confirm that `.env` exists and contains `GEMINI_API_KEY`.
- If Streamlit cannot start, make sure the virtual environment is activated and the dependencies are installed.
- If Gemini blocks a prompt for safety reasons, try rewriting the input in a more neutral way.