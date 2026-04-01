# Raj-Ni-Kshay | TB Adherence Monitoring System 🏥

**Raj-Ni-Kshay** is a smart healthcare intervention system built for the **Government of Rajasthan**. It automates medication adherence monitoring for Tuberculosis (TB) patients using a cost-effective "Missed Call" mechanism and a centralized administrative portal.



## 🌟 Key Features
* [cite_start]**Automated Alarms:** The system triggers automated voice calls to patients at two customizable daily intervals (e.g., Morning/Evening).
* [cite_start]**Missed Call Validation:** Patients "respond" to medication prompts by giving a missed call back to the system, which automatically updates their adherence record in the database.
* **Critical Alert Dashboard:** Real-time monitoring for health officers to identify patients who have missed 2 or more doses.
* **Official Registry:** Secure portal for registering new beneficiaries with Aadhaar and District-level categorization.

## 🛠️ Tech Stack
* **Frontend:** Streamlit (Python-based interactive dashboard).
* [cite_start]**Backend:** Flask (Webhook handling) & Schedule (Task automation).
* [cite_start]**Database:** Supabase (PostgreSQL with real-time capabilities).
* [cite_start]**Telephony:** Twilio API for automated Voice Calls and Webhooks.

## 🚀 Installation & Setup

### 1. Clone the Repository
git clone [https://github.com/atharvtamboli/TB_Gov_Project.git](https://github.com/atharvtamboli/TB_Gov_Project.git)
cd TB_Gov_Project

### 2. Configuration
Update the keys in gov_portal.py and call_engine.py:
Supabase: URL and Service Key.
Twilio: SID, Auth Token, and Twilio Phone Number.

### 3. Running the Application
You need two terminal windows:

Terminal 1 (The Portal): streamlit run gov_portal.py.
Terminal 2 (The Engine): python call_engine.py.

### 📊 Database Schema
The system relies on a Supabase backend with two primary tables:
patients: Stores full_name, phone_number, missed_doses, and alarm_time.

officers: Manages portal access with email and password authentication.

