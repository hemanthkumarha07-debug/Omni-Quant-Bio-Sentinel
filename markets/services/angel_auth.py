import os
import pyotp
from SmartApi import SmartConnect
from django.conf import settings

class AngelOneAuthService:
    def __init__(self):
        # Assuming you load your .env into Django settings or access os.environ directly
        self.api_key = os.getenv("ANGEL_API_KEY")
        self.client_id = os.getenv("ANGEL_CLIENT_ID")
        self.pin = os.getenv("ANGEL_PIN")
        self.totp_secret = os.getenv("ANGEL_TOTP_SECRET")
        self.smart_connect = SmartConnect(api_key=self.api_key)

    def generate_totp(self):
        """Generates the current valid TOTP based on the secret."""
        return pyotp.TOTP(self.totp_secret).now()

    def login_and_get_token(self):
        """Authenticates with Angel One and retrieves the JWT."""
        current_totp = self.generate_totp()
        
        try:
            session_data = self.smart_connect.generateSession(
                self.client_id, 
                self.pin, 
                current_totp
            )
            
            if session_data.get('status'):
                jwt_token = session_data['data']['jwtToken']
                refresh_token = session_data['data']['refreshToken']
                feed_token = session_data['data']['feedToken']
                
                # Here you can save the tokens to your ChromaDB, Redis, or just return them
                return {
                    "success": True,
                    "jwt_token": jwt_token,
                    "refresh_token": refresh_token,
                    "feed_token": feed_token
                }
            else:
                return {
                    "success": False,
                    "error": session_data.get('message', 'Unknown login error')
                }
                
        except Exception as e:
            return {"success": False, "error": str(e)}