from .config import settings
from supabase import create_client, Client

supabase: Client = create_client(str(settings.SUPABASE_URL), settings.SUPABASE_API_KEY.get_secret_value())

supabase_admin: Client | None = None
if settings.SUPABASE_SERVICE_ROLE_KEY:
    supabase_admin = create_client(str(settings.SUPABASE_URL), settings.SUPABASE_SERVICE_ROLE_KEY.get_secret_value())


if not supabase or supabase_admin is None:
    raise ValueError("Supabase client not initialized properly")