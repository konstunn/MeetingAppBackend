web: bin/start-pgbouncer-stunnel uvicorn MeetingApp.asgi:application --host 0.0.0.0 --port $PORT
worker: python manage.py runworker realtime-event-sender -v2