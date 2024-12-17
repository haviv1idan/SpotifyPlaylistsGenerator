FROM python:3.11-slim

WORKDIR /users

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["fastapi", "dev", "user_api.py", "--port", "8000", "--host", "0.0.0.0"]
