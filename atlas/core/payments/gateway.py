# atlas/core/payments/gateway.py
import requests

def delegate_stripe_charge(payment_token: str, amount_usd: float):
    # Enforces KRONOS-MEMORY-007: Leverage Stripe Tokenization instead of direct card handling
    charge_payload = {
        "source": payment_token,
        "amount": int(amount_usd * 100),
        "currency": "usd"
    }
    gateway_resp = requests.post("https://api.stripe.com/v1/charges", json=charge_payload)
    return gateway_resp.json()
