FROM python:3.11-slim

WORKDIR /users

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["fastapi", "run", "user_api.py"]
