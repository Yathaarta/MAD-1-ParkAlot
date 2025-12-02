# Vehicle-Parking-App - ParkAlot
Project for May-Term 2025 for MAD-1 course in diploma level in IIT-M BS Data Science Degree


## Project Description

This project implements a multi-user Vehicle Parking App, designed to efficiently manage parking lots and individual parking spots for 4-wheelers. The application aims to provide a seamless parking experience through a completely styled and responsive UI. It supports two primary roles:

* **Administrator:** Manages the entire parking infrastructure, including creating, editing, and deleting parking lots and individual spots, and monitoring overall system status.
* **User:** Can register, log in, search for available parking, book a spot (with automatic allocation), and manage their reservations by occupying or releasing spots. The system tracks real-time status updates and maintains a history of all parking activities.

## Features

### Admin Functionalities

* **Parking Lot Management:** Create new parking lots with specified capacity (which automatically creates spots), edit existing lot details, and delete lots (only if all spots are empty).
* **Parking Spot Management:** View detailed status of all spots within a lot, add new individual spots, and delete existing spots (only if no active or future bookings exist).
* **User Management:** View a list of all registered users and their basic details.
* **Platform Summary:** Access an overview of total users, parking lots, active bookings, and historical records. Includes a chart visualizing top booked lots from history.
* **Search Functionality:** Search for specific users by email/ID or parking lots by city/pincode.
* **Real-time Status Updates:** Admin views (dashboard, parking spots management) automatically trigger updates to spot statuses based on booking times to show the most current physical occupancy.

### User Functionalities

* **Registration & Login:** Secure user authentication with password hashing.
* **Parking Search:** Search for available parking lots based on city or pincode, viewing live occupancy statistics.
* **Spot Reservation:** Book a parking spot for a specified duration, with automatic allocation of the first available spot within the chosen lot and time.
* **Booking Management:** Occupy a spot (implicit by `parking_time` becoming current), and release/cancel bookings to free up the spot.
* **History Tracking:** View a comprehensive history of past parking sessions, including timestamps and costs.
* **User Summary:** Access a personalized summary of parking habits, including a chart of most frequently used parking lots from their history.
* **Profile Management:** Update personal details (username, email, password) and delete account (if no active/future bookings).

## Project Structure

The project follows a modular and organized directory structure:

```
root/
├── controllers/
│   ├── config.py                               # Application configuration settings
│   ├── decorators.py                           # Custom decorators for access control
│   └── routes.py                               # Defines all Flask routes and view logic
├── models/
│   └── dbmodel.py                              # SQLAlchemy database models and schema definitions
├── static/
│   ├── css/
│   │   ├── navbar2.css                         # Styles for navigation bar
│   │   └── parking_spot.css                    # Styles specific to parking spot display
│   ├── images/
│   │   └── (all images)                        # Project images (e.g., logo, background)
│   └── js/
│       └── parking_spot_scripts.js             # JavaScript for dynamic frontend interactions
├── templates/
│   └── (all HTML files)                        # Jinja2 HTML templates for rendering pages
├── .env                                        # Environment variables (e.g., database URI, secret key)
└── app.py                                      # Main Flask application instance and entry point
```

## Technologies Used

* **Backend:** Flask, Flask-SQLAlchemy, Werkzeug.security
* **Database:** SQLite
* **Frontend:** Jinja2 (templating), HTML, CSS, Bootstrap 5, JavaScript, Chart.js
* **Utilities:** python-dotenv, python-slugify

## How to Run

To run this project locally, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd vehicle-parking-app
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # On Windows:
    .\venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Create a `.env` file:** In the root directory of your project (where `app.py` is), create a file named `.env` and add the following lines:
    ```env
    SQLALCHEMY_DATABASE_URI=sqlite:///instance/parkalot.db
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SECRET_KEY='your_strong_random_key_here'      # Replace with a strong, random key
    ```
    *Note: The database file `parkalot.db` will be created automatically inside the `instance` folder when you first run the application.*
5.  **Run the Flask application:**
    ```bash
    flask run
    ```
    The application will typically be accessible at `http://127.0.0.1:5000/` in your web browser.

## Completed Milestones

Below is a list of completed milestones for this project:

* Milestone: Admin Dashboard and Lot/Spot Management
* Milestone: User Dashboard and Reservation/Parking System
* Milestone: Reservation/Parking History and Summary
* Milestone: Slot Time Calculation and Parking Cost
* Milestone: Search functionality for Admin
* Milestone: Charts and Visualization
* Milestone: Frontend and Backend Validation
* Milestone: Responsive UI and Styling
* Milestone: Flask Login Integration and Security
* Milestone: Persistent User Notification System

## Important Links

* Project Document: https://drive.google.com/file/d/1ITJMjlUXqFmRsfdUG01XgcTYtPFdYQV1/view?usp=sharing
* ER Diagram for Database model: https://drive.google.com/file/d/1qj3zjXXeYz34Xhmb28jjNe1-7p5vgZsi/view?usp=sharing
* Project Demostration Video: https://drive.google.com/file/d/1fvCD8g0ysJ_ebdIGmdNOivHzyuYIzCYZ/view?usp=sharing

## Screenshots

* Landing page

![alt text](https://github.com/user-attachments/assets/f2f3e914-b730-4f10-aec9-2c819a1a8839)

* Admin Dashboard, User home and parking spots

![alt text](https://github.com/user-attachments/assets/f03acb84-72f7-471f-99c7-47eaf61d3c66)
![alt text](https://github.com/user-attachments/assets/10999812-15c9-4fbf-b13f-6695f1794733)
![alt text](https://github.com/user-attachments/assets/48c19557-c119-4523-a00a-9a13bf76a969)
