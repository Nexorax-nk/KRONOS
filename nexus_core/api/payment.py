# src/api/payment.py
import requests

def process_transaction(token: str, amount: float):
    # Enforces KRONOS-MEMORY-007: Leverage Stripe Tokenization instead of direct card handling
    payload = {
        "source": token,
        "amount": int(amount * 100),
        "currency": "usd"
    }
    response = requests.post("https://api.stripe.com/v1/charges", json=payload)
    return response.json()
