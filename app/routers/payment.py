from time import timezone
from fastapi import APIRouter, Depends
from ..schemas import PaymentRequest, CheckoutRequest
from ..deps import get_current_user_id, get_user_token, get_auth_client
from ..services.payment_service import PaymentService 
from datetime import datetime, timezone
from ..db import supabase 


router = APIRouter(prefix="/payment", tags=["payment"])
@router.post("/create-order")
def create_order(req: CheckoutRequest, user = Depends(get_current_user_id)):
    if supabase:
        supabase.table('profiles').update({
            'selected_habits': req.habits,
            'duration_months': req.duration_months
        }).eq('id', user.id).execute()

    amount = req.duration_months * 500 * 100
    return PaymentService.create_order(amount)

@router.post("/verify")
def verify_payment(req: PaymentRequest,user = Depends(get_current_user_id), token: str = Depends(get_user_token)):
    PaymentService.verify_payment_and_activate_subscription(user.id, req)

    if supabase:
        profile = supabase.table('profiles').select('selected_habits').eq('id', user.id).single().execute().data
        habits = profile.get('selected_habits') if profile else []
        if habits:
            client = get_auth_client(token)
            now = datetime.now(timezone.utc).isoformat()
            tasks = [{
                'title': habit,
                'deadline': now,
                'completed': False,
                'user_id': user.id,
                'is_recurring': True 
            } for habit in habits]
            client.table('tasks').insert(tasks).execute()
    return {'status': 'success'}

