# DebussyVox

A voice interface framework for the DebussyOps Project.

## Voice Avatar Interface for DebussyOps (Complete Prototype)

This project allows you to speak to DebussyOps and see/hear a response via an animated avatar.

## Quick start (local)

1. Ensure DebussyOps is running and reachable at `http://localhost:8080/v1/query`. If it's elsewhere, set the `DEBUSSYOPS_URL` environment variable in `docker-compose.yml` or `backend/debussy_client.py`.

2. Build & run:
```bash
docker-compose up --build
```
3. Open the frontend
```
http://localhost:3000
```
4. Click Start Recording, speak a short sentence, stop recording. The UI will show the transcript and the avatar will speak the response.