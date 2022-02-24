FROM python:3.8.12

EXPOSE 443

COPY ./requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /app

CMD uvicorn app.main:app --host 0.0.0.0 --port 443 --ssl-keyfile=./privkey.pem --ssl-certfile=./fullchain.pem

# cd backend
# uvicorn app.main:app --host 0.0.0.0 --port 5051
