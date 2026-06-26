# Secure-Journey-AI 🛡️✈️

An AI-powered public safety web platform designed to protect women and tourists using real-time computer vision threat detection, secure database monitoring, and proactive alert systems. Built using Python, Django, and Machine Learning.

---

## 🚀 Features

*   **Real-Time Threat Detection:** Utilizes computer vision and machine learning models to detect potential safety risks and anomalies in real-time.
*   **Proactive Automated Alerts:** Integrates third-party APIs to instantly dispatch emergency notifications:
    *   **SMS Alerts:** Real-time SMS warning system powered by **Twilio**.
    *   **Email Notifications:** Instant email updates sent via secure SMTP configurations.
*   **Secure Infrastructure:** Developed with a modular architecture ensuring robust data handling, session management, and secure administrative dashboards.
*   **User-Friendly Interface:** Tailored dashboard for both civilian users/tourists and administrators monitoring active safety zones.

---

## 🛠️ Tech Stack

*   **Backend:** Python, Django Web Framework
*   **Machine Learning / Vision:** OpenCV, Computer Vision Models (YOLO)
*   **APIs & Services:** Twilio API (SMS), Django Core Mail (SMTP)
*   **Database:** SQLite / PostgreSQL

---

## 📂 Project Structure

```text
Secure-Journey-AI/
│
├── website/                 # Core Django project directory
│   ├── website/             # Project configuration (settings.py, urls.py)
│   ├── templates/           # Frontend HTML files
│   └── manage.py            # Django management script
│
├── requirements.txt         # Project dependencies and libraries
└── README.md                # Project documentation
