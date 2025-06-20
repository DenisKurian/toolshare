# TOOLSHARE — Community Tool Sharing Platform 🧰

TOOLSHARE is a Django-based web application that enables users to list, rent, and share tools with others in their local community. The platform encourages sustainable usage, cost efficiency, and convenience by allowing tools to be discovered and sorted based on physical proximity.

---

## 🚀 Features

- **User Authentication** — Sign up, log in, manage personal profiles and tool listings.
- **Proximity-Based Tool Browsing** — Users view tools sorted by distance using geolocation and the Haversine formula.
- **Tool Rentals & Dynamic Cancellation** — Book tools with date ranges and get partial refunds on cancellation based on timing.
- **Image Gallery & Ratings** — Upload images for tools and rate tools post-rental for quality assurance.
- **Live Chat & Bookmarks** — Communicate with tool owners and bookmark favorites for quick access.
- **Admin Dashboard** — View users, manage categories, respond to complaints, and monitor rental activity.

---

## 🛠️ Technologies

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, Bootstrap
- **Database**: SQLite (default), or PostgreSQL in production
- **Deployment**: Render
- **Geolocation**: Geopy + Haversine
- **Realtime UX**: AJAX for chat and booking updates

---

## 🧪 Local Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/toolshare.git
   cd toolshare