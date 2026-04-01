import time
import schedule
from datetime import datetime
from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client
from supabase import create_client

# --- CONFIGURATION (PASTE KEYS HERE) ---
SUPABASE_URL = "--"
SUPABASE_KEY = "--"
TWILIO_SID = "--"
TWILIO_AUTH = "--"
TWILIO_NUM = "--"

# Setup Clients
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
client = Client(TWILIO_SID, TWILIO_AUTH)
app = Flask(__name__)

# --- 1. THE WEBHOOK (Incoming Missed Call) ---
@app.route("/webhook", methods=['POST'])
def handle_incoming_call():
    caller = request.values.get('From')
    print(f"[INFO] Missed Call from {caller}")
    
    # Update Database
    supabase.table('patients').update({
        'missed_doses': 0, 
        'last_dose_date': 'now()'
    }).eq('phone_number', caller).execute()
    
    resp = VoiceResponse()
    resp.reject()
    return str(resp)

# --- 2. THE SCHEDULER (Checks for 2 Alarms) ---
def check_alarms():
    current_time = datetime.now().strftime("%H:%M")
    print(f"[SYSTEM] Scanning schedule for {current_time}...")

    try:
        # Fetch all active patients
        response = supabase.table("patients").select("*").execute()
        patients = response.data

        for p in patients:
            # Check Alarm 1 OR Alarm 2
            match_1 = (p.get('alarm_time') == current_time)
            match_2 = (p.get('alarm_time_2') == current_time)

            if match_1 or match_2:
                print(f" -> CALLING {p['full_name']} ({p['phone_number']})")
                
                # TRIGGER CALL
                try:
                    call = client.calls.create(
                        url="http://demo.twilio.com/docs/voice.xml", # Replace with Wagdi MP3 later
                        to=p['phone_number'],
                        from_=TWILIO_NUM
                    )
                    print(f"    Success! Call SID: {call.sid}")
                except Exception as e:
                    print(f"    Call Failed: {e}")
                    print("    (Tip: In Trial Mode, you can ONLY call your own verified number)")

    except Exception as e:
        print(f"Error reading DB: {e}")

# Run check every 60 seconds
schedule.every(1).minutes.do(check_alarms)

if __name__ == "__main__":
    print("--- RAJASTHAN TB MONITORING ENGINE STARTED ---")
    while True:
        schedule.run_pending()
        time.sleep(1)