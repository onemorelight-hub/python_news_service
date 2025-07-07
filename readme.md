# Method 1: Using uvicorn directly
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Method 2: Using Python
python main.py

# Method 3: Using FastAPI CLI (if installed)
fastapi dev main.py