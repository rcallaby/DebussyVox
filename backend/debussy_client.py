import os
import requests
import json

DEBUSSYOPS_URL = os.environ.get("DEBUSSYOPS_URL", "http://localhost:8080/v1/query")

def query_debussy(text):
    """
    Send { input: "<text>" } to DebussyOps and return the reply text.
    Adjust this if DebussyOps expects a different JSON shape.
    """
    payload = {"input": text}
    resp = requests.post(DEBUSSYOPS_URL, json=payload, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    # Try common fields for reply; adapt to DebussyOps output
    if isinstance(data, dict):
        return data.get("reply") or data.get("output") or data.get("result") or json.dumps(data)
    return str(data)
