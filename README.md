# README

## Authentication with flask-jwt-extended

### Development Server

gunicorn -b localhost:8000 wsgi:app

### Production Server

gunicorn -b 0.0.0.0:7000 -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 1 wsgi_production:app
