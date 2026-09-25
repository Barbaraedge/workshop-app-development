FROM python:3.12-slim

COPY src /app
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "-u", "motor_simulator.py"]
