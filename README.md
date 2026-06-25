# ♟️ Lichess Statistics Tracker (Work in Progress 🚧)

A Python-based automation tool designed to fetch, analyze, and track player statistics and rating changes using the official Lichess API. The application monitors specified player profiles, detects changes in game counts or ratings, and logs data locally.

**Current Project Status:** Active Development. The core API integration and data comparison logic are fully functional. The next phases include adding timestamps, automated email reports, and a graphical user interface (GUI).

---

## 🚀 Features

### Implemented
- **Lichess API Integration:** Secure authentication using API tokens via environment variables to fetch user profiles.
- **Dynamic Performance Tracking:** Automatically extracts statistics for specific game modes (Rapid, Blitz, Puzzles).
- **Data Persistence:** Saves and updates history in a local structured `stats.json` file.
- **Smart Delta Comparison:** Compares new API data against historical metrics to calculate precise rating changes (`+` or `-`) and total games played since the last check.

### Planned / Roadmap
- [ ] **Timestamping:** Integrate the `datetime` module to log the exact time of each performance snapshot.
- [ ] **Email Alerts:** Implement automated notifications via `smtplib` to send progress reports directly to a target email address when changes occur.
- [ ] **Graphical User Interface (GUI):** Transition from a CLI-based script to a desktop application (exploring Tkinter and moving towards a professional PyQt implementation).

---

## 💻 Tech Stack & Dependencies

* **Language:** Python 3.14.4
* **Libraries:**
  * `requests` (HTTP client for API interaction)
  * `python-dotenv` (Environment variable management)
  * `json` & `os` (Data processing and file system handling)

---

## ⚙️ Installation & Configuration

### 1. Prerequisites
Ensure you have Python 3.x installed on your system.

### 2. Clone the Repository
```bash
git clone https://github.com/Denys-Yashyn/Lichess-Stats-Tracker.git
```
```bash
cd Lichess-Stats-Tracker
```
### 3. Setup Environment Variables
To run this application, you need to configure your secrets locally.

Create a file named .env in the root directory.

Open the template file (e.g., env_example.txt or env.example) uploaded in the repository.

Copy its structure into your new .env file and populate it with your actual credentials:
```Plaintext
LICHESS_API_TOKEN=your_personal_lichess_token
EMAIL_SENDER=your_email@example.com
EMAIL_APP_PASSWORD=your_secure_app_password
TARGET_EMAIL=receiver_email@example.com
```
### 4. Customize Tracking Parameters
Before running the script, open `main.py` in your text editor and update the target users and game modes to fit your needs. 

Locate the following variables at the top of the file:
```python
# Change these to the Lichess usernames you want to track
user_names = ["Your_Username_Here", "Another_Player"]

# Customize the game modes (e.g., "bullet", "classic", "correspondence" More info about available modes is here: https://lichess.org/api#description/clients)
# inside the dictionary comprehension:
for mode in ["rapid", "puzzle", "blitz"]
```

### 5. Running the Script
Currently, the application runs via the command line:
```
python main.py
```
## 📂 Architecture Overview
`main.py` — The core execution script containing API request handling, dictionary comprehension for statistics, and delta comparison logic.

`env.example` — A safe template showcasing required environment variables without exposing sensitive tokens.

`.gitignore` — Configured to prevent local caching files (`__pycache__`), virtual environments (`venv`), and the confidential `.env` file from being exposed publicly.

`LICENSE` — Licensed under the permissive MIT License.

