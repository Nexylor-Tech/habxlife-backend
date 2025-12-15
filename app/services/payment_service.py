import razorpay
from datetime import datetime, timezone, timedelta
from fastapi import HTTPException
from ..config import settings
from ..db import supabase 

razorpay_client = razorpay.Client(
    auth=(settings.RAZORPAY_API_KEY.get_secret_value(), settings.RAZORPAY_TEST_KEY_SECRET.get_secret_value())
    if settings.RAZORPAY_API_KEY and settings.RAZORPAY_TEST_KEY_SECRET else None
)

class PaymentService:
    @staticmethod
    def create_order(amount: int, currency: str = "INR"):
        if not razorpay_client:
            raise HTTPException(status_code=503, detail="Razorpay client not initialized")
        order = razorpay_client.order.create({
            "amount": amount,
            "currency": currency,
            "receipt": f"rcpt_{datetime.utcnow().timestamp()}"
            # "receipt": str(uuid.uuid4()),
            # "notes": {
            #     "created_at": datetime.now(timezone.utc).isoformat()
            # }
        })
        return {
            'order_id': order['id'],
            'amount': order['amount'],
            'currency': order['currency'],
            'key_id': settings.RAZORPAY_API_KEY.get_secret_value(),
            # 'receipt': order['receipt']
        }
    @staticmethod
    def verify_payment_and_activate_subscription(user_id: str, req):
        if not razorpay_client:
            raise HTTPException(status_code=503)
        razorpay_client.utility.verify_payment_signature({
            'razorpay_order_id': req.razorpay_order_id,
            'razorpay_payment_id': req.razorpay_payment_id,
            'razorpay_signature': req.razorpay_signature
        })
        expiry = (datetime.now(timezone.utc) + timedelta(days=req.duration_months * 28)).isoformat()
        return supabase.table('profiles').update({
            'subscription_expiry': expiry,
            'onboarding_completed': True,
            'current_step': 'completed'
        }).eq('id', user_id).execute().data


