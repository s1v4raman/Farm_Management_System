import logging
import requests

logger = logging.getLogger(__name__)

def send_water_alert_sms(phone_number, message):
    if not phone_number:
        return False
        
    print(f"\n{'='*50}")
    print(f"📱 ATTEMPTING TO SEND REAL SMS ALERT")
    print(f"To: {phone_number}")
    print(f"Message: {message}")
    print(f"{'='*50}\n")
    
    try:
        # Using Textbelt.com free SMS API (1 free SMS per day per IP)
        resp = requests.post('https://textbelt.com/text', data={
          'phone': phone_number,
          'message': message,
          'key': 'textbelt',
        }, timeout=10)
        
        result = resp.json()
        print(f"SMS Gateway Response: {result}")
        return result.get('success', False)
    except Exception as e:
        print(f"Failed to send SMS via Textbelt: {e}")
        return False
