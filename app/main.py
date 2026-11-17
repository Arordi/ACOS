from __future__ import annotations

from contextlib import asynccontextmanager

import i18n.bootstrap

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app.api import router as api_router
from core.database import Base, engine
from models import Project, MediaFile


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    ACOS application startup and shutdown lifecycle.
    """

    Base.metadata.create_all(
        bind=engine
    )

    yield


app = FastAPI(
    title="ACOS",
    description=(
        "AI Creative Operating System"
    ),
    version="0.1.0",
    lifespan=lifespan,
)


# ---------------------------------------------------------
# API ROUTERS
# ---------------------------------------------------------

app.include_router(
    api_router
)


# ---------------------------------------------------------
# MAIN WEBSITE
# ---------------------------------------------------------

@app.get(
    "/",
    response_class=HTMLResponse,
)
def home():
    return """
    <!DOCTYPE html>

    <html lang="en">

    <head>

        <meta charset="UTF-8">

        <meta
            name="viewport"
            content="width=device-width, initial-scale=1.0"
        >

        <meta
            name="description"
            content="ACOS — AI Creative Operating System. A professional AI platform for creative, film, media, translation and production workflows."
        >

        <meta
            name="robots"
            content="index, follow"
        >

        <meta
            name="application-name"
            content="ACOS"
        >

        <meta
            name="theme-color"
            content="#111827"
        >

        <link
            rel="canonical"
            href="https://acos.onrender.com/"
        >

        <title>
            ACOS — AI Creative Operating System
        </title>


        <!-- Open Graph -->

        <meta
            property="og:type"
            content="website"
        >

        <meta
            property="og:title"
            content="ACOS — AI Creative Operating System"
        >

        <meta
            property="og:description"
            content="AI Creative Operating System for creative, film, media and multilingual workflows."
        >

        <meta
            property="og:url"
            content="https://acos.onrender.com/"
        >

        <meta
            property="og:site_name"
            content="ACOS"
        >


        <!-- Twitter / X -->

        <meta
            name="twitter:card"
            content="summary"
        >

        <meta
            name="twitter:title"
            content="ACOS — AI Creative Operating System"
        >

        <meta
            name="twitter:description"
            content="AI Creative Operating System for creative, film, media and multilingual workflows."
        >


        <!-- Structured Data -->

        <script type="application/ld+json">
        {
            "@context": "https://schema.org",
            "@type": "WebApplication",
            "name": "ACOS",
            "description": "AI Creative Operating System",
            "url": "https://acos.onrender.com/",
            "applicationCategory": "MultimediaApplication",
            "operatingSystem": "Web",
            "inLanguage": "en"
        }
        </script>


        <style>

            * {
                box-sizing: border-box;
            }

            body {
                margin: 0;

                font-family:
                    Arial,
                    Helvetica,
                    sans-serif;

                background: #111827;

                color: white;

                min-height: 100vh;
            }

            .container {
                max-width: 1000px;

                margin: 0 auto;

                padding:
                    70px
                    20px;
            }

            h1 {
                font-size: 52px;

                margin:
                    0 0 12px;
            }

            .subtitle {
                color: #cbd5e1;

                font-size: 22px;

                line-height: 1.6;

                max-width: 800px;
            }

            .card {
                margin-top: 40px;

                padding: 30px;

                background: #1f2937;

                border-radius: 18px;
            }

            .status {
                color: #4ade80;

                font-weight: bold;

                font-size: 18px;
            }

            .description {
                color: #cbd5e1;

                line-height: 1.7;

                font-size: 17px;
            }

            .links {
                margin-top: 25px;
            }

            .links a {
                color: #93c5fd;

                text-decoration: none;

                margin-right: 20px;
            }

            .links a:hover {
                text-decoration: underline;
            }

        </style>

    </head>


    <body>

        <main class="container">

            <h1>
                ACOS
            </h1>

            <p class="subtitle">
                AI Creative Operating System
            </p>


            <section class="card">

                <h2>
                    System Status
                </h2>

                <p class="status">
                    ● ACOS is running
                </p>

                <p class="description">
                    ACOS is a professional AI operating
                    system for creative, film, media,
                    multilingual and production workflows.
                </p>


                <div class="links">

                    <a href="/docs">
                        API Documentation
                    </a>

                    <a href="/api/health">
                        System Health
                    </a>

                </div>

            </section>

        </main>

    </body>

    </html>
    """


# ---------------------------------------------------------
# HEALTH CHECK
# ---------------------------------------------------------

@app.get(
    "/api/health"
)
def health():

    return {
        "status": "ok",

        "application": "ACOS",

        "version": "0.1.0",

        "database": "connected",
    }
