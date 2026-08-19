import os
import requests
from dotenv import load_dotenv

# Load environment variables securely
load_dotenv()
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

def send_alert(message):
    if not DISCORD_WEBHOOK_URL:
        return {"success": False, "error": "Discord Webhook URL is missing in .env file."}
        
    payload = {
        "content": message
    }
    
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        # Discord returns 204 No Content on successful webhook execution
        if response.status_code in [200, 204]:
            return {"success": True, "data": "Alert sent successfully via Discord."}
        else:
            return {"success": False, "error": f"Discord API Error: {response.text}"}
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    print("Discord Alert System Module is ready.")