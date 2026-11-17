from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(
    title="ACOS",
    description="AI Creative Operating System",
    version="0.1.0"
)


@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html lang="hy">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ACOS — AI Creative Operating System</title>
        <style>
            body {
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app.api import router as api_router


app = FastAPI(
    title="ACOS",
    description="AI Creative Operating System",
    version="0.1.0",
)

app.include_router(api_router)


@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html lang="hy">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ACOS — AI Creative Operating System</title>

        <style>
            body {
                margin: 0;
                font-family: Arial, sans-serif;
                background: #111827;
                color: white;
            }

            .container {
                max-width: 900px;
                margin: 0 auto;
                padding: 60px 20px;
            }

            h1 {
                font-size: 48px;
                margin-bottom: 10px;
            }

            p {
                color: #cbd5e1;
                font-size: 20px;
            }

            .card {
                margin-top: 35px;
                padding: 25px;
                background: #1f2937;
                border-radius: 16px;
            }

            .status {
                color: #4ade80;
                font-weight: bold;
            }
        </style>
    </head>

    <body>
        <div class="container">

            <h1>ACOS</h1>

            <p>
                AI Creative Operating System
            </p>

            <div class="card">

                <h2>System Status</h2>

                <p class="status">
                    ● ACOS is running
                </p>

                <p>
                    CreativeOS core is ready for development.
                </p>

            </div>

        </div>
    </body>
    </html>
    """


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "application": "ACOS",
        "version": "0.1.0",
    }
