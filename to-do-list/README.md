# To-Do List API with Front-End

This is a simple to-do list application with a back-end API built using **FastAPI** and a basic front-end using HTML, CSS, and JavaScript.

---

## Features
- [Features](#features)
- [Installation](#installation)
- [API Endpoints](#api-endpoints)
- [Technologies Used](#technologies-used)
---

## Installation

### Prerequisites
- Python 3.8+ installed

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/makooster/to-do-list.git
   cd todo-list-api

2. Create a virtual environment and activate it
    ```bash 
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies
    ```bash 
    python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

4. Run the server
    ```bash
     uvicorn main:app --reload

5. Open the app
- API Documentation: http://127.0.0.1:8000/docs
- Front-End: http://127.0.0.1:8000/static/index.html

---

## API Endpoints
| Method   | Endpoint           | Description                 | Example Request Body       |
|----------|--------------------|-----------------------------|----------------------------|
| `GET`    | `/tasks/`          | Retrieve all tasks          | N/A                        |
| `POST`   | `/tasks/`          | Add a new task              | `{ "id": 1, "title": "Task" }` |
| `PUT`    | `/tasks/{task_id}` | Update an existing task     | `{ "title": "Updated Task" }` |
| `DELETE` | `/tasks/{task_id}` | Delete a specific task      | N/A                        |


## Technologies used
- Back-End: FastAPI
- Front-End: HTML, CSS, JavaScript
- API Documentation: Swagger UI