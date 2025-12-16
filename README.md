# Raja Mantri Chor Sipahi - Game Engine

A backend logic engine for the classic Indian childhood game "Raja Mantri Chor Sipahi," built with **FastAPI**.

## 🚀 Features
- **Multiplayer Logic:** Handles 4-player sessions via REST API.
- **Role Shuffling:** Conflict-free randomization of roles (Raja, Mantri, Chor, Sipahi).
- **Scoring Engine:** Automated point calculation based on the Mantri's guess.
- **Error Handling:** Robust validation for invalid moves or unauthorized actions.

## 🛠️ Tech Stack
- **Language:** Python
- **Framework:** FastAPI
- **Server:** Uvicorn

## ⚙️ How to Run
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the server: `uvicorn main:app --reload`
