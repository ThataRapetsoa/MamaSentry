# MamaSentry

MamaSentry is a lightweight fraud detection service that cleans incoming text, checks for suspicious patterns, and returns a risk score and matched triggers.

## Project structure

- app/utils/text_cleaner.py — text normalization for fraud analysis
- app/fraud/patterns.py — suspicious keywords and phrase matching
- app/routes/fraud.py — business logic entry point for fraud checks
- app/schemas/fraud.py — request/response schemas
- main.py — FastAPI application entrypoint

## Quick start

1. Create and activate a virtual environment
2. Install dependencies:
   pip install -r requirements.txt
3. Run the app:
   uvicorn main:app --reload
4. Open the API docs:
   http://127.0.0.1:8000/docs

## Example request

POST /check-fraud

{
  "message": "URGENT!!! Send 5000 now to verify your account."
}

## Example response

{
  "suspicious": true,
  "risk_score": 8,
  "matches": ["urgent", "verify", "send", "account"],
  "cleaned_message": "urgent send 5000 now to verify your account"
}
