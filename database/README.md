# run mongo docker 
```bash
docker run -d --name mongodb -p 27017:27017 mongo
```

# run fastapi 
## without docker
```bash
fastapi dev user_api.py
```

## with docker
```bash
# build
docker build -t users_api:latest .


```
