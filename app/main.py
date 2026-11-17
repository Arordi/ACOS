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
        "ACOS — AI Creative Operating System "
        "for film, media and creative production."
    ),
    version="0.2.0",
    lifespan=lifespan,
)


# =========================================================
# API ROUTERS
# =========================================================

app.include_router(
    api_router
)


# =========================================================
# MAIN WEBSITE
# =========================================================

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
        content="ACOS — AI Creative Operating System for creating films, stories, characters, scenes, video, voice, music and multilingual content."
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
        content="#08090c"
    >

    <link
        rel="canonical"
        href="https://acos.onrender.com/"
    >

    <title>
        ACOS — AI Film Studio
    </title>


    <!-- =====================================================
         OPEN GRAPH
    ====================================================== -->

    <meta
        property="og:type"
        content="website"
    >

    <meta
        property="og:title"
        content="ACOS — AI Film Studio"
    >

    <meta
        property="og:description"
        content="Create films, stories, characters, scenes, video, voice, music and multilingual content with ACOS."
    >

    <meta
        property="og:url"
        content="https://acos.onrender.com/"
    >

    <meta
        property="og:site_name"
        content="ACOS"
    >


    <!-- =====================================================
         TWITTER
    ====================================================== -->

    <meta
        name="twitter:card"
        content="summary"
    >

    <meta
        name="twitter:title"
        content="ACOS — AI Film Studio"
    >

    <meta
        name="twitter:description"
        content="Create films with ACOS — AI Creative Operating System."
    >


    <!-- =====================================================
         STRUCTURED DATA
    ====================================================== -->

    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": "ACOS",
        "description": "AI Creative Operating System for film and creative production.",
        "url": "https://acos.onrender.com/",
        "applicationCategory": "MultimediaApplication",
        "operatingSystem": "Web",
        "inLanguage": "en"
    }
    </script>


    <style>

        /* =====================================================
           RESET
        ====================================================== */

        * {
            box-sizing: border-box;
        }


        html {
            scroll-behavior: smooth;
        }


        body {
            margin: 0;

            min-height: 100vh;

            background:
                radial-gradient(
                    circle at 70% 10%,
                    rgba(124, 58, 237, 0.12),
                    transparent 32%
                ),
                radial-gradient(
                    circle at 15% 70%,
                    rgba(37, 99, 235, 0.08),
                    transparent 30%
                ),
                #08090c;

            color: #f8fafc;

            font-family:
                Inter,
                ui-sans-serif,
                system-ui,
                -apple-system,
                BlinkMacSystemFont,
                "Segoe UI",
                sans-serif;

            overflow-x: hidden;
        }


        button,
        input,
        textarea {
            font: inherit;
        }


        button {
            cursor: pointer;
        }


        a {
            color: inherit;
            text-decoration: none;
        }


        /* =====================================================
           APP LAYOUT
        ====================================================== */

        .app {
            min-height: 100vh;

            display: grid;

            grid-template-columns:
                250px
                minmax(0, 1fr);
        }


        /* =====================================================
           SIDEBAR
        ====================================================== */

        .sidebar {
            position: fixed;

            left: 0;
            top: 0;
            bottom: 0;

            width: 250px;

            display: flex;

            flex-direction: column;

            padding: 22px 16px;

            background:
                rgba(10, 11, 15, 0.94);

            border-right:
                1px solid
                rgba(255, 255, 255, 0.07);

            backdrop-filter:
                blur(20px);

            z-index: 20;
        }


        .brand {
            display: flex;

            align-items: center;

            gap: 12px;

            padding:
                4px
                10px
                28px;
        }


        .brand-mark {
            width: 38px;
            height: 38px;

            border-radius: 12px;

            display: grid;

            place-items: center;

            background:
                linear-gradient(
                    135deg,
                    #8b5cf6,
                    #4f46e5
                );

            box-shadow:
                0 8px 30px
                rgba(99, 102, 241, 0.25);

            font-weight: 900;

            letter-spacing: -1px;
        }


        .brand-name {
            font-size: 20px;

            font-weight: 800;

            letter-spacing: -0.5px;
        }


        .brand-subtitle {
            display: block;

            margin-top: 2px;

            color: #64748b;

            font-size: 10px;

            text-transform: uppercase;

            letter-spacing: 1.5px;
        }


        .nav {
            display: flex;

            flex-direction: column;

            gap: 4px;

            overflow-y: auto;
        }


        .nav-title {
            margin:
                18px
                10px
                7px;

            color: #475569;

            font-size: 10px;

            font-weight: 700;

            text-transform: uppercase;

            letter-spacing: 1.4px;
        }


        .nav-item {
            display: flex;

            align-items: center;

            gap: 12px;

            width: 100%;

            padding:
                10px
                12px;

            border: 1px solid transparent;

            border-radius: 10px;

            background: transparent;

            color: #94a3b8;

            text-align: left;

            transition:
                0.2s ease;
        }


        .nav-item:hover {
            color: #f8fafc;

            background:
                rgba(255, 255, 255, 0.05);
        }


        .nav-item.active {
            color: #ffffff;

            background:
                linear-gradient(
                    90deg,
                    rgba(124, 58, 237, 0.22),
                    rgba(124, 58, 237, 0.06)
                );

            border-color:
                rgba(139, 92, 246, 0.18);
        }


        .nav-icon {
            width: 20px;

            text-align: center;

            font-size: 16px;
        }


        .sidebar-bottom {
            margin-top: auto;

            padding-top: 16px;
        }


        .system-status {
            padding: 13px;

            border:
                1px solid
                rgba(255, 255, 255, 0.06);

            border-radius: 12px;

            background:
                rgba(255, 255, 255, 0.025);
        }


        .status-row {
            display: flex;

            align-items: center;

            gap: 8px;

            color: #94a3b8;

            font-size: 12px;
        }


        .status-dot {
            width: 7px;
            height: 7px;

            border-radius: 50%;

            background: #22c55e;

            box-shadow:
                0 0 12px
                rgba(34, 197, 94, 0.7);
        }


        .status-text {
            margin-top: 7px;

            color: #475569;

            font-size: 10px;
        }


        /* =====================================================
           MAIN
        ====================================================== */

        .main {
            grid-column: 2;

            min-width: 0;

            padding:
                0
                28px
                50px;
        }


        /* =====================================================
           TOPBAR
        ====================================================== */

        .topbar {
            position: sticky;

            top: 0;

            height: 72px;

            display: flex;

            align-items: center;

            justify-content: space-between;

            border-bottom:
                1px solid
                rgba(255, 255, 255, 0.05);

            background:
                rgba(8, 9, 12, 0.82);

            backdrop-filter:
                blur(20px);

            z-index: 10;
        }


        .breadcrumb {
            color: #64748b;

            font-size: 13px;
        }


        .breadcrumb strong {
            color: #e2e8f0;
        }


        .top-actions {
            display: flex;

            align-items: center;

            gap: 10px;
        }


        .icon-button {
            width: 38px;
            height: 38px;

            border:
                1px solid
                rgba(255, 255, 255, 0.08);

            border-radius: 10px;

            background:
                rgba(255, 255, 255, 0.03);

            color: #94a3b8;
        }


        .icon-button:hover {
            color: #ffffff;

            background:
                rgba(255, 255, 255, 0.07);
        }


        .avatar {
            width: 38px;
            height: 38px;

            display: grid;

            place-items: center;

            border-radius: 50%;

            background:
                linear-gradient(
                    135deg,
                    #334155,
                    #111827
                );

            border:
                1px solid
                rgba(255, 255, 255, 0.1);

            color: #e2e8f0;

            font-size: 13px;

            font-weight: 700;
        }


        /* =====================================================
           HERO
        ====================================================== */

        .hero {
            padding:
                58px
                0
                36px;
        }


        .eyebrow {
            display: inline-flex;

            align-items: center;

            gap: 8px;

            padding:
                7px
                11px;

            border:
                1px solid
                rgba(139, 92, 246, 0.2);

            border-radius: 999px;

            color: #c4b5fd;

            background:
                rgba(124, 58, 237, 0.08);

            font-size: 11px;

            font-weight: 700;

            text-transform: uppercase;

            letter-spacing: 1px;
        }


        .hero h1 {
            max-width: 760px;

            margin:
                18px
                0
                12px;

            font-size:
                clamp(
                    38px,
                    5vw,
                    64px
                );

            line-height: 1.02;

            letter-spacing: -2.8px;

            font-weight: 850;
        }


        .hero h1 span {
            background:
                linear-gradient(
                    90deg,
                    #ffffff,
                    #a78bfa,
                    #60a5fa
                );

            -webkit-background-clip: text;

            background-clip: text;

            color: transparent;
        }


        .hero p {
            max-width: 700px;

            margin: 0;

            color: #94a3b8;

            font-size: 17px;

            line-height: 1.7;
        }


        .hero-actions {
            display: flex;

            gap: 12px;

            margin-top: 26px;

            flex-wrap: wrap;
        }


        .primary-button {
            padding:
                13px
                20px;

            border: 0;

            border-radius: 10px;

            background:
                linear-gradient(
                    135deg,
                    #8b5cf6,
                    #6366f1
                );

            color: white;

            font-weight: 750;

            box-shadow:
                0 12px 30px
                rgba(99, 102, 241, 0.22);

            transition:
                0.2s ease;
        }


        .primary-button:hover {
            transform: translateY(-1px);

            box-shadow:
                0 16px 35px
                rgba(99, 102, 241, 0.32);
        }


        .secondary-button {
            padding:
                13px
                20px;

            border:
                1px solid
                rgba(255, 255, 255, 0.09);

            border-radius: 10px;

            background:
                rgba(255, 255, 255, 0.035);

            color: #e2e8f0;

            font-weight: 650;
        }


        .secondary-button:hover {
            background:
                rgba(255, 255, 255, 0.07);
        }


        /* =====================================================
           WORKSPACE
        ====================================================== */

        .workspace {
            display: grid;

            grid-template-columns:
                minmax(0, 1.7fr)
                minmax(280px, 0.8fr);

            gap: 18px;

            margin-top: 18px;
        }


        .panel {
            border:
                1px solid
                rgba(255, 255, 255, 0.07);

            border-radius: 16px;

            background:
                rgba(255, 255, 255, 0.025);

            overflow: hidden;
        }


        .panel-header {
            display: flex;

            align-items: center;

            justify-content: space-between;

            padding:
                15px
                17px;

            border-bottom:
                1px solid
                rgba(255, 255, 255, 0.06);
        }


        .panel-title {
            font-size: 13px;

            font-weight: 750;
        }


        .panel-label {
            color: #64748b;

            font-size: 11px;
        }


        /* =====================================================
           VIDEO PREVIEW
        ====================================================== */

        .preview {
            position: relative;

            aspect-ratio: 16 / 9;

            min-height: 320px;

            display: flex;

            align-items: center;

            justify-content: center;

            background:
                radial-gradient(
                    circle at 50% 40%,
                    rgba(99, 102, 241, 0.2),
                    transparent 30%
                ),
                linear-gradient(
                    145deg,
                    #111827,
                    #050608
                );
        }


        .preview-grid {
            position: absolute;

            inset: 0;

            opacity: 0.16;

            background-image:
                linear-gradient(
                    rgba(255,255,255,0.06)
                    1px,
                    transparent 1px
                ),
                linear-gradient(
                    90deg,
                    rgba(255,255,255,0.06)
                    1px,
                    transparent 1px
                );

            background-size:
                45px
                45px;
        }


        .play-button {
            position: relative;

            width: 76px;
            height: 76px;

            display: grid;

            place-items: center;

            border-radius: 50%;

            border:
                1px solid
                rgba(255, 255, 255, 0.18);

            background:
                rgba(255, 255, 255, 0.08);

            color: white;

            font-size: 25px;

            padding-left: 4px;

            backdrop-filter:
                blur(15px);

            transition:
                0.2s ease;
        }


        .play-button:hover {
            transform: scale(1.05);

            background:
                rgba(139, 92, 246, 0.28);
        }


        .preview-empty {
            position: absolute;

            bottom: 22px;

            left: 22px;

            color: #64748b;

            font-size: 11px;
        }


        /* =====================================================
           QUICK ACTIONS
        ====================================================== */

        .quick-actions {
            display: grid;

            grid-template-columns:
                repeat(4, 1fr);

            gap: 10px;

            padding: 15px;
        }


        .quick-card {
            padding: 16px;

            border:
                1px solid
                rgba(255, 255, 255, 0.06);

            border-radius: 12px;

            background:
                rgba(255, 255, 255, 0.025);

            transition:
                0.2s ease;
        }


        .quick-card:hover {
            transform: translateY(-2px);

            border-color:
                rgba(139, 92, 246, 0.25);

            background:
                rgba(139, 92, 246, 0.06);
        }


        .quick-icon {
            margin-bottom: 10px;

            font-size: 20px;
        }


        .quick-title {
            color: #e2e8f0;

            font-size: 12px;

            font-weight: 700;
        }


        .quick-text {
            margin-top: 4px;

            color: #64748b;

            font-size: 10px;

            line-height: 1.5;
        }


        /* =====================================================
           RIGHT PROJECT PANEL
        ====================================================== */

        .project-panel {
            padding-bottom: 16px;
        }


        .project-content {
            padding: 18px;
        }


        .project-title {
            font-size: 19px;

            font-weight: 800;

            letter-spacing: -0.4px;
        }


        .project-description {
            margin-top: 7px;

            color: #64748b;

            font-size: 12px;

            line-height: 1.6;
        }


        .progress {
            height: 5px;

            margin-top: 20px;

            overflow: hidden;

            border-radius: 999px;

            background:
                rgba(255, 255, 255, 0.06);
        }


        .progress-bar {
            width: 8%;

            height: 100%;

            border-radius: inherit;

            background:
                linear-gradient(
                    90deg,
                    #8b5cf6,
                    #60a5fa
                );
        }


        .workflow {
            margin-top: 20px;

            display: flex;

            flex-direction: column;
        }


        .workflow-step {
            position: relative;

            display: flex;

            align-items: center;

            gap: 12px;

            padding:
                9px
                0;
        }


        .workflow-step:not(:last-child)::after {
            content: "";

            position: absolute;

            left: 11px;

            top: 32px;

            width: 1px;

            height: 20px;

            background:
                rgba(255, 255, 255, 0.08);
        }


        .step-dot {
            width: 23px;
            height: 23px;

            display: grid;

            place-items: center;

            border-radius: 50%;

            border:
                1px solid
                rgba(255, 255, 255, 0.1);

            background:
                #111827;

            color: #64748b;

            font-size: 9px;

            z-index: 1;
        }


        .workflow-step.active .step-dot {
            background:
                #7c3aed;

            border-color:
                #8b5cf6;

            color: white;

            box-shadow:
                0 0 16px
                rgba(124, 58, 237, 0.35);
        }


        .step-name {
            color: #94a3b8;

            font-size: 12px;
        }


        .workflow-step.active .step-name {
            color: #ffffff;

            font-weight: 700;
        }


        /* =====================================================
           STORYBOARD
        ====================================================== */

        .storyboard {
            margin-top: 18px;
        }


        .scene-grid {
            display: grid;

            grid-template-columns:
                repeat(4, minmax(0, 1fr));

            gap: 12px;

            padding: 16px;
        }


        .scene {
            min-width: 0;

            border:
                1px solid
                rgba(255, 255, 255, 0.06);

            border-radius: 12px;

            overflow: hidden;

            background:
                rgba(255, 255, 255, 0.02);
        }


        .scene-image {
            aspect-ratio: 16 / 9;

            display: grid;

            place-items: center;

            background:
                linear-gradient(
                    135deg,
                    #182033,
                    #090b10
                );

            color: #475569;

            font-size: 11px;
        }


        .scene-info {
            padding: 10px;
        }


        .scene-number {
            color: #64748b;

            font-size: 9px;

            text-transform: uppercase;

            letter-spacing: 1px;
        }


        .scene-name {
            margin-top: 4px;

            color: #cbd5e1;

            font-size: 11px;

            font-weight: 650;

            white-space: nowrap;

            overflow: hidden;

            text-overflow: ellipsis;
        }


        /* =====================================================
           TIMELINE
        ====================================================== */

        .timeline {
            margin-top: 18px;

            padding-bottom: 18px;
        }


        .timeline-body {
            padding:
                18px;
        }


        .timeline-ruler {
            display: flex;

            justify-content: space-between;

            color: #475569;

            font-size: 9px;

            margin-bottom: 9px;
        }


        .timeline-track {
            height: 48px;

            display: flex;

            gap: 4px;

            padding: 4px;

            border-radius: 8px;

            background:
                rgba(255, 255, 255, 0.025);

            border:
                1px solid
                rgba(255, 255, 255, 0.05);
        }


        .timeline-clip {
            height: 100%;

            border-radius: 5px;

            background:
                linear-gradient(
                    135deg,
                    rgba(124, 58, 237, 0.5),
                    rgba(79, 70, 229, 0.28)
                );

            border:
                1px solid
                rgba(139, 92, 246, 0.25);
        }


        .clip-one {
            width: 18%;
        }


        .clip-two {
            width: 27%;
        }


        .clip-three {
            width: 21%;
        }


        .clip-four {
            width: 16%;
        }


        /* =====================================================
           FEATURES
        ====================================================== */

        .features {
            display: grid;

            grid-template-columns:
                repeat(3, 1fr);

            gap: 14px;

            margin-top: 18px;
        }


        .feature {
            padding: 20px;

            border:
                1px solid
                rgba(255, 255, 255, 0.06);

            border-radius: 14px;

            background:
                rgba(255, 255, 255, 0.02);
        }


        .feature-icon {
            font-size: 22px;

            margin-bottom: 13px;
        }


        .feature h3 {
            margin: 0;

            font-size: 14px;
        }


        .feature p {
            margin:
                7px
                0
                0;

            color: #64748b;

            font-size: 11px;

            line-height: 1.6;
        }


        /* =====================================================
           MOBILE
        ====================================================== */

        .mobile-menu {
            display: none;
        }


        @media (max-width: 1100px) {

            .app {
                grid-template-columns: 215px minmax(0, 1fr);
            }

            .sidebar {
                width: 215px;
            }

            .workspace {
                grid-template-columns: 1fr;
            }

            .quick-actions {
                grid-template-columns:
                    repeat(2, 1fr);
            }

        }


        @media (max-width: 800px) {

            .app {
                display: block;
            }

            .sidebar {
                transform:
                    translateX(-100%);

                transition:
                    transform 0.25s ease;
            }

            .sidebar.open {
                transform:
                    translateX(0);
            }

            .main {
                padding:
                    0
                    16px
                    40px;
            }

            .mobile-menu {
                display: grid;
            }

            .hero {
                padding-top: 40px;
            }

            .scene-grid {
                grid-template-columns:
                    repeat(2, 1fr);
            }

            .features {
                grid-template-columns: 1fr;
            }

        }


        @media (max-width: 520px) {

            .hero h1 {
                font-size: 40px;

                letter-spacing: -1.8px;
            }

            .hero p {
                font-size: 15px;
            }

            .quick-actions {
                grid-template-columns: 1fr;
            }

            .scene-grid {
                grid-template-columns: 1fr;
            }

            .topbar {
                height: 64px;
            }

        }

    </style>

</head>


<body>


<div class="app">


    <!-- =====================================================
         SIDEBAR
    ====================================================== -->

    <aside
        class="sidebar"
        id="sidebar"
    >

        <div class="brand">

            <div class="brand-mark">
                A
            </div>

            <div>

                <div class="brand-name">
                    ACOS
                </div>

                <span class="brand-subtitle">
                    Creative OS
                </span>

            </div>

        </div>


        <nav class="nav">


            <div class="nav-title">
                Create
            </div>


            <button
                class="nav-item active"
                onclick="selectNav(this)"
            >

                <span class="nav-icon">
                    ✦
                </span>

                <span>
                    New Film
                </span>

            </button>


            <button
                class="nav-item"
                onclick="selectNav(this)"
            >

                <span class="nav-icon">
                    ▣
                </span>

                <span>
                    Projects
                </span>

            </button>


            <div class="nav-title">
                Story
            </div>


            <button
                class="nav-item"
                onclick="selectNav(this)"
            >

                <span class="nav-icon">
                    ✎
                </span>

                <span>
                    Script
                </span>

            </button>


            <button
                class="nav-item"
                onclick="selectNav(this)"
            >

                <span class="nav-icon">
                    ◉
                </span>

                <span>
                    Characters
                </span>

            </button>


            <button
                class="nav-item"
                onclick="selectNav(this)"
            >

                <span class="nav-icon">
                    ▤
                </span>

                <span>
                    Storyboard
                </span>

            </button>


            <button
                class="nav-item"
                onclick="selectNav(this)"
            >

                <span class="nav-icon">
                    ◇
                </span>

                <span>
                    Scenes
                </span>

            </button>


            <div class="nav-title">
                Production
            </div>


            <button
                class="nav-item"
                onclick="selectNav(this)"
            >

                <span class="nav-icon">
                    ▶
                </span>

                <span>
                    Video
                </span>

            </button>


            <button
                class="nav-item"
                onclick="selectNav(this)"
            >

                <span class="nav-icon">
                    ♪
                </span>

                <span>
                    Voice
                </span>

            </button>


            <button
                class="nav-item"
                onclick="selectNav(this)"
            >

                <span class="nav-icon">
                    ♫
                </span>

                <span>
                    Music
                </span>

            </button>


            <div class="nav-title">
                Localize
            </div>


            <button
                class="nav-item"
                onclick="selectNav(this)"
            >

                <span class="nav-icon">
                    文
                </span>

                <span>
                    Languages
                </span>

            </button>


            <button
                class="nav-item"
                onclick="selectNav(this)"
            >

                <span class="nav-icon">
                    ◌
                </span>

                <span>
                    Dubbing
                </span>

            </button>


            <button
                class="nav-item"
                onclick="selectNav(this)"
            >

                <span class="nav-icon">
                    ▥
                </span>

                <span>
                    Subtitles
                </span>

            </button>


            <div class="nav-title">
                Export
            </div>


            <button
                class="nav-item"
                onclick="selectNav(this)"
            >

                <span class="nav-icon">
                    ↓
                </span>

                <span>
                    Render Film
                </span>

            </button>


        </nav>


        <div class="sidebar-bottom">

            <div class="system-status">

                <div class="status-row">

                    <span class="status-dot"></span>

                    <span>
                        ACOS Core Online
                    </span>

                </div>

                <div class="status-text">
                    CreativeOS v0.2
                </div>

            </div>

        </div>

    </aside>


    <!-- =====================================================
         MAIN
    ====================================================== -->

    <main class="main">


        <!-- TOPBAR -->

        <header class="topbar">

            <div
                class="breadcrumb"
            >

                <strong>
                    ACOS
                </strong>

                <span>
                    &nbsp; / &nbsp; Studio
                </span>

            </div>


            <div class="top-actions">

                <button
                    class="icon-button mobile-menu"
                    onclick="toggleSidebar()"
                    aria-label="Open menu"
                >
                    ☰
                </button>

                <button
                    class="icon-button"
                    onclick="openDocs()"
                    aria-label="Documentation"
                >
                    ?
                </button>

                <button
                    class="icon-button"
                    onclick="openHealth()"
                    aria-label="System health"
                >
                    ●
                </button>

                <div class="avatar">
                    A
                </div>

            </div>

        </header>


        <!-- HERO -->

        <section class="hero">

            <span class="eyebrow">
                ✦ AI Creative Operating System
            </span>


            <h1>
                Create a film
                <span>
                    from imagination.
                </span>
            </h1>


            <p>
                ACOS brings story, characters, scenes,
                video, voice, music and multilingual
                production into one creative workspace.
            </p>


            <div class="hero-actions">

                <button
                    class="primary-button"
                    onclick="startFilm()"
                >
                    ✦ Create New Film
                </button>


                <button
                    class="secondary-button"
                    onclick="importScript()"
                >
                    Import Script
                </button>

            </div>

        </section>


        <!-- WORKSPACE -->

        <section class="workspace">


            <!-- LEFT / PREVIEW -->

            <div>


                <div class="panel">

                    <div class="panel-header">

                        <div class="panel-title">
                            Film Preview
                        </div>

                        <div class="panel-label">
                            16:9 • Cinematic
                        </div>

                    </div>


                    <div class="preview">

                        <div
                            class="preview-grid"
                        ></div>


                        <button
                            class="play-button"
                            onclick="previewFilm()"
                            aria-label="Preview film"
                        >
                            ▶
                        </button>


                        <div class="preview-empty">
                            Your generated film will appear here.
                        </div>

                    </div>


                    <div class="quick-actions">


                        <button
                            class="quick-card"
                            onclick="quickAction('script')"
                        >

                            <div class="quick-icon">
                                ✎
                            </div>

                            <div class="quick-title">
                                Write Script
                            </div>

                            <div class="quick-text">
                                Turn an idea into a screenplay.
                            </div>

                        </button>


                        <button
                            class="quick-card"
                            onclick="quickAction('characters')"
                        >

                            <div class="quick-icon">
                                ◉
                            </div>

                            <div class="quick-title">
                                Build Characters
                            </div>

                            <div class="quick-text">
                                Create consistent film characters.
                            </div>

                        </button>


                        <button
                            class="quick-card"
                            onclick="quickAction('storyboard')"
                        >

                            <div class="quick-icon">
                                ▤
                            </div>

                            <div class="quick-title">
                                Storyboard
                            </div>

                            <div class="quick-text">
                                Plan every shot and scene.
                            </div>

                        </button>


                        <button
                            class="quick-card"
                            onclick="quickAction('video')"
                        >

                            <div class="quick-icon">
                                ▶
                            </div>

                            <div class="quick-title">
                                Generate Video
                            </div>

                            <div class="quick-text">
                                Turn scenes into cinematic video.
                            </div>

                        </button>


                    </div>

                </div>


                <!-- STORYBOARD -->

                <div class="panel storyboard">

                    <div class="panel-header">

                        <div class="panel-title">
                            Storyboard
                        </div>

                        <div class="panel-label">
                            4 scenes
                        </div>

                    </div>


                    <div class="scene-grid">


                        <div class="scene">

                            <div class="scene-image">
                                Scene preview
                            </div>

                            <div class="scene-info">

                                <div class="scene-number">
                                    Scene 01
                                </div>

                                <div class="scene-name">
                                    Opening
                                </div>

                            </div>

                        </div>


                        <div class="scene">

                            <div class="scene-image">
                                Scene preview
                            </div>

                            <div class="scene-info">

                                <div class="scene-number">
                                    Scene 02
                                </div>

                                <div class="scene-name">
                                    The Encounter
                                </div>

                            </div>

                        </div>


                        <div class="scene">

                            <div class="scene-image">
                                Scene preview
                            </div>

                            <div class="scene-info">

                                <div class="scene-number">
                                    Scene 03
                                </div>

                                <div class="scene-name">
                                    The Conflict
                                </div>

                            </div>

                        </div>


                        <div class="scene">

                            <div class="scene-image">
                                Scene preview
                            </div>

                            <div class="scene-info">

                                <div class="scene-number">
                                    Scene 04
                                </div>

                                <div class="scene-name">
                                    Resolution
                                </div>

                            </div>

                        </div>


                    </div>

                </div>


                <!-- TIMELINE -->

                <div class="panel timeline">

                    <div class="panel-header">

                        <div class="panel-title">
                            Timeline
                        </div>

                        <div class="panel-label">
                            00:00 — 02:40
                        </div>

                    </div>


                    <div class="timeline-body">

                        <div class="timeline-ruler">

                            <span>
                                00:00
                            </span>

                            <span>
                                00:30
                            </span>

                            <span>
                                01:00
                            </span>

                            <span>
                                01:30
                            </span>

                            <span>
                                02:00
                            </span>

                            <span>
                                02:40
                            </span>

                        </div>


                        <div class="timeline-track">

                            <div
                                class="timeline-clip clip-one"
                            ></div>

                            <div
                                class="timeline-clip clip-two"
                            ></div>

                            <div
                                class="timeline-clip clip-three"
                            ></div>

                            <div
                                class="timeline-clip clip-four"
                            ></div>

                        </div>

                    </div>

                </div>


            </div>


            <!-- RIGHT / PROJECT -->

            <aside>


                <div class="panel project-panel">


                    <div class="panel-header">

                        <div class="panel-title">
                            Current Film
                        </div>

                        <div class="panel-label">
                            Draft
                        </div>

                    </div>


                    <div class="project-content">


                        <div class="project-title">
                            Untitled Film
                        </div>


                        <div class="project-description">
                            Start with an idea and build
                            your film step by step.
                        </div>


                        <div class="progress">

                            <div
                                class="progress-bar"
                            ></div>

                        </div>


                        <div class="workflow">


                            <div
                                class="workflow-step active"
                            >

                                <div class="step-dot">
                                    1
                                </div>

                                <div class="step-name">
                                    Idea
                                </div>

                            </div>


                            <div
                                class="workflow-step"
                            >

                                <div class="step-dot">
                                    2
                                </div>

                                <div class="step-name">
                                    Script
                                </div>

                            </div>


                            <div
                                class="workflow-step"
                            >

                                <div class="step-dot">
                                    3
                                </div>

                                <div class="step-name">
                                    Characters
                                </div>

                            </div>


                            <div
                                class="workflow-step"
                            >

                                <div class="step-dot">
                                    4
                                </div>

                                <div class="step-name">
                                    Storyboard
                                </div>

                            </div>


                            <div
                                class="workflow-step"
                            >

                                <div class="step-dot">
                                    5
                                </div>

                                <div class="step-name">
                                    Scenes
                                </div>

                            </div>


                            <div
                                class="workflow-step"
                            >

                                <div class="step-dot">
                                    6
                                </div>

                                <div class="step-name">
                                    Video
                                </div>

                            </div>


                            <div
                                class="workflow-step"
                            >

                                <div class="step-dot">
                                    7
                                </div>

                                <div class="step-name">
                                    Voice
                                </div>

                            </div>


                            <div
                                class="workflow-step"
                            >

                                <div class="step-dot">
                                    8
                                </div>

                                <div class="step-name">
                                    Music
                                </div>

                            </div>


                            <div
                                class="workflow-step"
                            >

                                <div class="step-dot">
                                    9
                                </div>

                                <div class="step-name">
                                    Translation
                                </div>

                            </div>


                            <div
                                class="workflow-step"
                            >

                                <div class="step-dot">
                                    10
                                </div>

                                <div class="step-name">
                                    Final Film
                                </div>

                            </div>


                        </div>

                    </div>

                </div>


            </aside>


        </section>


        <!-- FEATURES -->

        <section class="features">


            <div class="feature">

                <div class="feature-icon">
                    🎬
                </div>

                <h3>
                    Film Creation
                </h3>

                <p>
                    Build an entire production from
                    concept to final film inside one workspace.
                </p>

            </div>


            <div class="feature">

                <div class="feature-icon">
                    🧠
                </div>

                <h3>
                    AI Creative Engine
                </h3>

                <p>
                    Connect multiple AI providers for
                    generation, analysis and quality control.
                </p>

            </div>


            <div class="feature">

                <div class="feature-icon">
                    🌍
                </div>

                <h3>
                    Global Localization
                </h3>

                <p>
                    Translate, dub and subtitle films
                    for audiences around the world.
                </p>

            </div>


        </section>


    </main>

</div>


<script>

    function toggleSidebar() {

        const sidebar =
            document.getElementById("sidebar");

        sidebar.classList.toggle("open");
    }


    function selectNav(element) {

        document
            .querySelectorAll(".nav-item")
            .forEach(
                item => item.classList.remove("active")
            );

        element.classList.add("active");

        if (
            window.innerWidth <= 800
        ) {

            document
                .getElementById("sidebar")
                .classList.remove("open");

        }

    }


    function startFilm() {

        alert(
            "ACOS Film Studio: New Film workflow will open here."
        );

    }


    function importScript() {

        alert(
            "Script import will be connected to the ACOS project API."
        );

    }


    function previewFilm() {

        alert(
            "Film preview will be connected to the generated media."
        );

    }


    function quickAction(action) {

        const names = {

            script: "Script",

            characters: "Characters",

            storyboard: "Storyboard",

            video: "Video Generation"

        };

        alert(
            "ACOS " +
            names[action] +
            " module will open here."
        );

    }


    function openDocs() {

        window.location.href = "/docs";

    }


    function openHealth() {

        window.location.href = "/api/health";

    }

</script>


</body>

</html>
"""


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get(
    "/api/health"
)
def health():

    return {
        "status": "ok",
        "application": "ACOS",
        "version": "0.2.0",
        "database": "connected",
    }
