FROM python:3.8-slim



RUN apt-get update && apt-get install -y \
    pkg-config \
    libhdf5-dev \
    gcc \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*


RUN pip install -r requirements.txt


COPY . .


EXPOSE 5000


ENV FLASK_APP=src/server.py


CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]
