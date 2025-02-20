# Weather API

This project provides a simple weather API that fetches real-time weather data from OpenWeatherMap.

## Features
- Retrieve weather data for a given city.
- Uses Django Rest Framework (DRF) for API implementation.
- Fetches data from OpenWeatherMap API.
- Simple token-based authentication (currently disabled).

## Installation

### 1. Clone the Repository
```sh
git clone https://github.com/makooster/back-projects.git
cd weatherapi
```

### 2. Create and Activate a Virtual Environment
```sh
python -m venv .venv
source .venv/bin/activate  # On macOS/Linux
.venv\Scripts\activate  # On Windows
```

### 3. Install Dependencies
```sh
pip install -r requirements.txt
```

### 4. Apply Migrations
```sh
python manage.py migrate
```

### 5. Run the Development Server
```sh
python manage.py runserver
```

## API Endpoints

### Get Weather Data
**Endpoint:**
```
GET /api/weather/{city_name}/
```

**Example Request:**
```sh
curl -X GET http://127.0.0.1:8000/api/weather/Pavlodar/
```

**Response:**
```json
{
    "city": "Pavlodar",
    "temperature": 5.2,
    "weather": "Clear",
    "humidity": 65,
    "wind_speed": 3.5
}
```

### Authentication (Optional, Currently Disabled)
If authentication is enabled, you can obtain a token using:
```sh
curl -X POST http://127.0.0.1:8000/api/token-auth/ \
     -H "Content-Type: application/json" \
     -d '{ "username": "your_username", "password": "your_password" }'
```

## Configuration
- API keys for OpenWeatherMap should be stored in environment variables or a `.env` file.
- Update `settings.py` to configure API keys and authentication.

## Project Structure
```
weatherapi/
│-- api/
│   │-- views.py  # API views
│   │-- urls.py   # API routes
│   │-- serializers.py  # DRF serializers
│-- weatherapi/
│   │-- settings.py  # Django settings
│   │-- urls.py  # Project routes
│-- .venv/  # Virtual environment
│-- manage.py  # Django management script
```

## Troubleshooting
### Common Errors & Fixes
1. **401 Unauthorized**: Ensure authentication is disabled in `settings.py` or provide a valid token.
2. **ConnectionError**: Check your internet connection and OpenWeatherMap API availability.
3. **Invalid City Name**: Ensure the city name is correctly spelled and supported by OpenWeatherMap.

## License
This project is licensed under the MIT License.

---
