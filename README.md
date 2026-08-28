# SKU Triage

Simple Flask app to upload a CSV of SKUs and perform a triage search.

Run locally:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Endpoints:
- `GET /` UI
- `POST /upload` form-data file=CSV (csv headers: sku,description,stock)
- `POST /triage` JSON `{ "sku": "text" }`

Deploy to Render (recommended):

1. Push this repo to GitHub (already at https://github.com/gabodrax32/inversa).
2. Go to https://render.com and sign in.
3. Create a new Web Service and connect your GitHub account, or let Render detect the `render.yaml` in this repository.
   - Select the `sku-triage` service (Docker) and the `main` branch.
4. Render will build the Docker image using the provided `Dockerfile` and deploy it. After deployment, Render provides a public URL like `https://sku-triage.onrender.com`.

Alternative: deploy with Docker locally

```powershell
cd C:\Users\gabri\sku-triage
docker build -t sku-triage:latest .
docker run -p 5000:5000 sku-triage:latest
# open http://localhost:5000
```

Notes:
- If you prefer a temporary public URL, use `ngrok` locally: `ngrok http 5000` (requires ngrok authtoken).
