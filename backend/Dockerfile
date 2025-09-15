FROM python:3.11-slim

WORKDIR /app

# system deps for ffmpeg may not be required; speech_recognition for some formats
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# create static dir for audio files
RUN mkdir -p ./static/audio

EXPOSE 5000
CMD ["python", "app.py"]
