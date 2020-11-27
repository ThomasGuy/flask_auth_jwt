# README

## Authentication with flask-jwt-extended

### Development Server

gunicorn -b localhost:7000 wsgi:app

### Production Server

gunicorn -b 0.0.0.0:6000 -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 1 wsgi_production:app

### JWT Authentication with flask-jwt-extended

Start development server

gunicorn -b localhost:7080 wsgi:app
