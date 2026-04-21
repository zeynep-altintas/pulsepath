# PulsePath

PulsePath is a web-based festival navigation and crowd intelligence tool. It provides live location-based crowd tracking, personal artist scheduling, and organiser dashboards with footfall analytics.

## Features

- Real-time crowd density tracking
- Interactive map with facility and stage icons
- Personal lineup selection for attendees
- Smart notifications based on schedule and crowd levels
- Admin dashboard for live monitoring and simulations

## Local Setup

To run PulsePath locally, follow the steps below.

### 1. Clone the Repository

```bash
git clone https://gitlab.computing.dcu.ie/sulajl2/2025-csc1118-sulajl2-altintz2.git
cd 2025-csc1118-sulajl2-altintz2

### 2. Clone the Repository

python -m venv venv
source venv/Scripts/activate  # Windows

### 3. Install Dependencies

pip install -r requirements.txt

### 4. Set up Environment Variables

DB_NAME=pulsepath
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432

### 5. Apply Migrations

python manage.py migrate

### 6. Run the Development Server

python manage.py runserver
Visit http://127.0.0.1:8000 in your browser.


