# Parking Management System

## Overview

The Parking Management System is a web application designed to manage and monitor parking spaces using computer vision. The system allows users to manage their parking history, view vehicle details, and administrators to manage parking rates and blacklisted vehicles.

## Features

- **User Management**: Register and manage user accounts.
- **Parking Management**: Track parking duration, calculate costs, and manage parking rates.
- **Vehicle Recognition**: Identify and manage vehicles using license plate recognition.
- **Reporting**: Generate CSV reports of parking records.
- **Email Notifications**: Notify users if parking costs exceed limits.

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy
- **Database**: PostgreSQL
- **Computer Vision**: OpenCV, TensorFlow/Keras
- **Authentication**: JWT-based
- **Containerization**: Docker, Docker Compose

## Setup

### Prerequisites

- Docker and Docker Compose
- Python 3.11+
- Poetry (for Python dependency management)

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Oleksandr-Arshynov/parking-management-system
   cd parking-management-system

2. python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. poetry install

4. docker-compose up --build


## Usage
Start the server:

The application will be available at http://localhost:8000.

## Access the Swagger UI:

Navigate to http://localhost:8000/docs to view and interact with the API documentation.

API Endpoints
User Endpoints
Get Current User Info

# GET /user

Retrieves information about the currently authenticated user.

Get User Plate

# GET /user/my_plate

Retrieves the license plate associated with the currently authenticated user.

Get Parking History

# GET /user/parking_history

Retrieves the parking history for the currently authenticated user.

Admin Endpoints
Add Plate

# POST /admin/add_plate

Adds a new vehicle plate to the system. Requires admin privileges.

Delete Plate

# DELETE /admin/delete_plate/{license_plate}

Deletes a vehicle plate from the system. Requires admin privileges.

Set Parking Rate

# PUT /admin/set_rate

Updates the parking rate for a specified plate. Requires admin privileges.

Blacklist Vehicle

# PUT /admin/blacklist/{license_plate}

Blacklists or unblacklists a vehicle based on its license plate. Requires admin privileges.

Parking Endpoints
Get Image

# POST /parking/get_image/

Processes an uploaded image to recognize the license plate and handle parking entry or exit.

Generate Report

# GET /report/generate-report/

Generates a CSV report of all parking records.

Email Endpoints
Check Parking Cost and Send Email

# GET /message-email/check-cost-email/{license_plate}

Checks if the parking cost for a vehicle has exceeded the limit and sends an email notification.

Development
For development, you can run the application locally and use the FastAPI Swagger UI to test endpoints. Ensure that the necessary environment variables are set and the database is properly configured.

Contributing
Contributions are welcome! Please open issues or submit pull requests to the repository.


