# Stark Industries Global Hackathon Portal

A highly interactive, Marvel-cinematic-universe-inspired registration system built for the GeeksForGeeks Bennett Chapter hackathon. This project bridges the gap between front-end immersive design and functional backend architecture, featuring a custom physics-based scrollbar, J.A.R.V.I.S.-style strict form validation, and a Python-powered API.

## 🚀 Features

*   **Cinematic Preloader:** A Marvel intro video sequence that seamlessly transitions into a high-tech engineering dashboard using GSAP animations[cite: 2].
*   **Interactive Spider-Man Scrollbar:** A custom-engineered, draggable scrollbar featuring Spider-Man swinging on a web, tied dynamically to the window's scroll percentage and drag physics[cite: 2].
*   **J.A.R.V.I.S. Strict Validation:** Front-end logic enforcing precise Regex patterns for names, emails, and squad designations to prevent gibberish submissions[cite: 2].
*   **Dynamic Squad Assembly:** A multi-page architecture that caches Commander data in the browser and auto-populates the team roster on the next page[cite: 4].
*   **Marvel Tech Classes:** Operatives select roles mapped to Marvel characters (e.g., Iron Man for Systems Architect, Shuri for UI/UX Design)[cite: 4].
*   **RESTful Python Backend:** A lightweight Flask server that handles atomic data persistence, securely saving team registrations to a JSON file.

## 🛠️ Tech Stack

**Frontend:**
*   HTML5 & CSS3
*   Tailwind CSS (via CDN for rapid styling)[cite: 2]
*   GSAP (GreenSock Animation Platform)[cite: 2]
*   Vanilla JavaScript (DOM manipulation, LocalStorage API, Custom Physics)[cite: 2, 4]

**Backend:**
*   Python 3[cite: 3]
*   Flask (Web framework & API routing)[cite: 3]
*   Flask-CORS (Cross-Origin Resource Sharing)[cite: 3]

## 📂 File Structure

*   `index.html` - The main landing page, mission briefing, and initial Commander registration[cite: 2].
*   `squad.html` - The secondary interface for adding up to three additional operatives to the roster[cite: 4].
*   `server.py` - The Flask backend script that serves the application and processes `POST` requests to `/api/register`[cite: 3].
*   `registrations.json` - Automatically generated database file storing validated team entries[cite: 3].
*   *Assets:* Requires `marvel_intro.mp4`, `stark_tower.jpg`, and `spiderman-hanging.png` in the root directory.
