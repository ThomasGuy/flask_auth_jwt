# README

## Authentication with flask-jwt-extended

### Development Server

gunicorn -b localhost:7000 wsgi:app

### Production Server

gunicorn -b 0.0.0.0:7000 -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 1 wsgi_production:app

### JWT Authentication with flask-jwt-extended

Start development server without socketio working

gunicorn -b localhost:7080 wsgi:app

or with Socketio firing:

gunicorn -b 0.0.0.0:7000 -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 1 wsgi:app

Alternativly set .flaskenv to development and use flask shell to play with the database
