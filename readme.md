# Method 1: Using uvicorn directly
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Method 2: Using Python
python main.py

# Method 3: Using FastAPI CLI (if installed)
fastapi dev main.py

# Get paginated news
curl "http://localhost:8000/api/v1/news?page=1&page_size=10"

# Search for articles
curl "http://localhost:8000/api/v1/news/search?q=european%20stocks&page=1"

# Get today's news
curl "http://localhost:8000/api/v1/news?date_range=today"

# Get news from specific source
curl "http://localhost:8000/api/v1/news?source_name=Yahoo"