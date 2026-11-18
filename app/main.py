from __future__ import annotations

from contextlib import asynccontextmanager

import i18n.bootstrap

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app.api import router as api_router
from core.database import Base, engine
from models import Project, MediaFile


# =========================================================
# APPLICATION LIFESPAN
# =========================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    ACOS application startup and shutdown lifecycle.
    """

    Base.metadata.create_all(
        bind=engine
    )

    yield


# =========================================================
# FASTAPI APPLICATION
# =========================================================

app = FastAPI(
    title="ACOS",
    description=(
        "ACOS — AI Creative Operating System "
        "for film, media and creative production."
    ),
    version="0.3.0",
    lifespan=lifespan,
)


# =========================================================
# API ROUTERS
# =========================================================

app.include_router(
    api_router
)


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
        "version": "0.3.0",
        "database": "connected",
    }


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
        name="theme-color"
        content="#080a10"
    >

    <meta
        name="description"
        content="ACOS — AI Creative Operating System for film, media and creative production."
    >

    <title>
        ACOS — Creative Studio
    </title>


    <style>

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
                    circle at 20% 0%,
                    rgba(124, 58, 237, 0.12),
                    transparent 28%
                ),
                radial-gradient(
                    circle at 85% 15%,
                    rgba(59, 130, 246, 0.09),
                    transparent 25%
                ),
                #080a10;

            color: #e5e7eb;

            font-family:
                Inter,
                ui-sans-serif,
                system-ui,
                -apple-system,
                BlinkMacSystemFont,
                "Segoe UI",
                sans-serif;

            -webkit-font-smoothing: antialiased;
        }


        button,
        input,
        textarea,
        select {
            font: inherit;
        }


        button {
            border: 0;
        }


        .app {
            min-height: 100vh;

            display: grid;

            grid-template-columns:
                250px
                minmax(0, 1fr);
        }


        /* =====================================================
           SIDEBAR
           ===================================================== */

        .sidebar {
            position: fixed;

            top: 0;
            left: 0;
            bottom: 0;

            width: 250px;

            padding: 20px 14px;

            display: flex;
            flex-direction: column;

            background:
                linear-gradient(
                    180deg,
                    rgba(12, 15, 24, 0.98),
                    rgba(7, 9, 15, 0.98)
                );

            border-right:
                1px solid
                rgba(255, 255, 255, 0.06);

            z-index: 100;
        }


        .brand {
            display: flex;
            align-items: center;

            gap: 11px;

            padding: 5px 9px 22px;
        }


        .brand-mark {
            width: 34px;
            height: 34px;

            display: grid;
            place-items: center;

            border-radius: 10px;

            background:
                linear-gradient(
                    135deg,
                    #7c3aed,
                    #4f46e5
                );

            box-shadow:
                0 0 28px
                rgba(124, 58, 237, 0.32);

            font-size: 16px;
            font-weight: 900;

            color: white;
        }


        .brand-name {
            color: #f8fafc;

            font-size: 16px;

            font-weight: 850;

            letter-spacing: -0.4px;
        }


        .brand-subtitle {
            margin-top: 2px;

            color: #475569;

            font-size: 9px;

            letter-spacing: 1.3px;

            text-transform: uppercase;
        }


        .nav-section {
            margin-top: 13px;
        }


        .nav-label {
            padding:
                0
                10px
                8px;

            color: #475569;

            font-size: 9px;

            font-weight: 700;

            letter-spacing: 1.5px;

            text-transform: uppercase;
        }


        .nav-item {
            width: 100%;

            display: flex;
            align-items: center;

            gap: 10px;

            padding:
                9px
                10px;

            margin-bottom: 2px;

            border-radius: 9px;

            background: transparent;

            color: #64748b;

            cursor: pointer;

            text-align: left;

            transition:
                background .18s ease,
                color .18s ease,
                transform .18s ease;
        }


        .nav-item:hover {
            background:
                rgba(255, 255, 255, 0.04);

            color: #cbd5e1;

            transform: translateX(2px);
        }


        .nav-item.active {
            background:
                linear-gradient(
                    90deg,
                    rgba(124, 58, 237, 0.16),
                    rgba(124, 58, 237, 0.05)
                );

            color: #ffffff;

            box-shadow:
                inset 2px 0 0 #8b5cf6;
        }


        .nav-icon {
            width: 20px;

            text-align: center;

            font-size: 13px;

            opacity: .9;
        }


        .nav-text {
            font-size: 11px;

            font-weight: 650;
        }


        .sidebar-spacer {
            flex: 1;
        }


        .system-status {
            margin: 10px 5px 3px;

            padding: 12px;

            border:
                1px solid
                rgba(255, 255, 255, 0.06);

            border-radius: 12px;

            background:
                rgba(255, 255, 255, 0.025);
        }


        .system-status-row {
            display: flex;
            align-items: center;

            gap: 7px;

            color: #94a3b8;

            font-size: 10px;
        }


        .status-dot {
            width: 7px;
            height: 7px;

            border-radius: 50%;

            background: #22c55e;

            box-shadow:
                0 0 10px
                rgba(34, 197, 94, 0.65);
        }


        .system-version {
            margin-top: 5px;

            color: #475569;

            font-size: 9px;
        }


        /* =====================================================
           MAIN
           ===================================================== */

        .main {
            min-width: 0;

            margin-left: 250px;

            padding:
                0
                28px
                60px;
        }


        .topbar {
            height: 70px;

            display: flex;
            align-items: center;

            justify-content: space-between;

            border-bottom:
                1px solid
                rgba(255, 255, 255, 0.045);
        }


        .topbar-left {
            display: flex;
            align-items: center;

            gap: 12px;
        }


        .breadcrumb {
            color: #64748b;

            font-size: 11px;
        }


        .breadcrumb strong {
            color: #cbd5e1;
        }


        .topbar-actions {
            display: flex;
            align-items: center;

            gap: 8px;
        }


        /* Language Selector UI */
        .language-select-wrapper {
            position: relative;
            display: inline-flex;
            align-items: center;
        }

        .language-select {
            height: 34px;
            padding: 0 10px;
            border: 1px solid rgba(255, 255, 255, 0.07);
            border-radius: 9px;
            background: rgba(255, 255, 255, 0.025);
            color: #94a3b8;
            cursor: pointer;
            font-size: 11px;
            font-weight: 650;
            outline: none;
            transition: background .18s ease, color .18s ease, border-color .18s ease;
        }

        .language-select:hover {
            background: rgba(255, 255, 255, 0.06);
            color: white;
            border-color: rgba(255, 255, 255, 0.12);
        }

        .language-select option {
            background: #111522;
            color: #e2e8f0;
        }


        .top-button {
            min-width: 34px;
            height: 34px;

            padding: 0 10px;

            display: inline-flex;
            align-items: center;
            justify-content: center;

            gap: 6px;

            border:
                1px solid
                rgba(255, 255, 255, 0.07);

            border-radius: 9px;

            background:
                rgba(255, 255, 255, 0.025);

            color: #94a3b8;

            cursor: pointer;

            transition:
                background .18s ease,
                color .18s ease,
                border-color .18s ease;
        }


        .top-button:hover {
            background:
                rgba(255, 255, 255, 0.06);

            color: white;

            border-color:
                rgba(255, 255, 255, 0.12);
        }


        .health-button {
            color: #86efac;
        }


        .avatar {
            width: 34px;
            height: 34px;

            display: grid;
            place-items: center;

            border-radius: 50%;

            background:
                linear-gradient(
                    135deg,
                    #312e81,
                    #7c3aed
                );

            color: white;

            font-size: 11px;

            font-weight: 800;
        }


        .mobile-menu {
            display: none;
        }


        /* =====================================================
           HERO
           ===================================================== */

        .hero {
            padding:
                72px
                0
                42px;
        }


        .hero-eyebrow {
            display: inline-flex;
            align-items: center;

            gap: 7px;

            padding:
                6px
                10px;

            border:
                1px solid
                rgba(139, 92, 246, 0.22);

            border-radius: 999px;

            background:
                rgba(124, 58, 237, 0.07);

            color: #a78bfa;

            font-size: 9px;

            font-weight: 750;

            letter-spacing: 1.3px;

            text-transform: uppercase;
        }


        .hero h1 {
            max-width: 800px;

            margin:
                18px
                0
                14px;

            color: #f8fafc;

            font-size: clamp(
                46px,
                6vw,
                76px
            );

            line-height: .98;

            letter-spacing: -4px;

            font-weight: 850;
        }


        .hero h1 span {
            background:
                linear-gradient(
                    100deg,
                    #ffffff,
                    #a78bfa 52%,
                    #60a5fa
                );

            -webkit-background-clip: text;
            background-clip: text;

            color: transparent;
        }


        .hero p {
            max-width: 650px;

            margin: 0;

            color: #64748b;

            font-size: 15px;

            line-height: 1.75;
        }


        .hero-actions {
            display: flex;

            flex-wrap: wrap;

            gap: 10px;

            margin-top: 26px;
        }


        .primary-button,
        .secondary-button {
            min-height: 42px;

            padding:
                0
                16px;

            display: inline-flex;
            align-items: center;
            justify-content: center;

            gap: 8px;

            border-radius: 10px;

            cursor: pointer;

            font-size: 11px;

            font-weight: 750;

            transition:
                transform .18s ease,
                box-shadow .18s ease,
                background .18s ease;
        }


        .primary-button {
            background:
                linear-gradient(
                    135deg,
                    #7c3aed,
                    #4f46e5
                );

            color: white;

            box-shadow:
                0 12px 30px
                rgba(79, 70, 229, 0.22);
        }


        .primary-button:hover {
            transform: translateY(-2px);

            box-shadow:
                0 17px 38px
                rgba(79, 70, 229, 0.32);
        }


        .secondary-button {
            border:
                1px solid
                rgba(255, 255, 255, 0.08);

            background:
                rgba(255, 255, 255, 0.025);

            color: #cbd5e1;
        }


        .secondary-button:hover {
            transform: translateY(-2px);

            background:
                rgba(255, 255, 255, 0.06);
        }


        /* =====================================================
           PANELS
           ===================================================== */

        .workspace {
            display: grid;

            grid-template-columns:
                minmax(0, 1fr)
                285px;

            gap: 18px;
        }


        .panel {
            overflow: hidden;

            border:
                1px solid
                rgba(255, 255, 255, 0.06);

            border-radius: 14px;

            background:
                linear-gradient(
                    180deg,
                    rgba(255, 255, 255, 0.025),
                    rgba(255, 255, 255, 0.012)
                );

            box-shadow:
                0 20px 60px
                rgba(0, 0, 0, 0.12);
        }


        .panel-header {
            min-height: 48px;

            display: flex;
            align-items: center;

            justify-content: space-between;

            padding:
                0
                16px;

            border-bottom:
                1px solid
                rgba(255, 255, 255, 0.045);
        }


        .panel-title {
            color: #e2e8f0;

            font-size: 11px;

            font-weight: 800;

            letter-spacing: -.1px;
        }


        .panel-label {
            color: #475569;

            font-size: 9px;

            font-weight: 650;
        }


        /* =====================================================
           PREVIEW
           ===================================================== */

        .preview {
            min-height: 430px;
        }


        .preview-screen {
            position: relative;

            aspect-ratio: 16 / 9;

            min-height: 300px;

            display: grid;
            place-items: center;

            background:
                radial-gradient(
                    circle at center,
                    rgba(124, 58, 237, 0.08),
                    transparent 40%
                ),
                linear-gradient(
                    135deg,
                    #101522,
                    #07090d
                );
        }


        .preview-empty {
            text-align: center;

            color: #475569;
        }


        .preview-empty-icon {
            width: 52px;
            height: 52px;

            margin: 0 auto 12px;

            display: grid;
            place-items: center;

            border:
                1px solid
                rgba(255, 255, 255, 0.06);

            border-radius: 50%;

            background:
                rgba(255, 255, 255, 0.025);

            color: #64748b;

            font-size: 17px;
        }


        .preview-empty-title {
            color: #64748b;

            font-size: 11px;

            font-weight: 700;
        }


        .preview-empty-text {
            margin-top: 5px;

            color: #334155;

            font-size: 9px;
        }


        .preview-play {
            position: absolute;

            left: 50%;
            top: 50%;

            transform:
                translate(-50%, -50%);

            width: 48px;
            height: 48px;

            display: grid;
            place-items: center;

            border:
                1px solid
                rgba(255, 255, 255, 0.08);

            border-radius: 50%;

            background:
                rgba(5, 7, 12, 0.72);

            color: white;

            cursor: pointer;

            opacity: .88;

            transition:
                transform .18s ease,
                background .18s ease;
        }


        .preview-play:hover {
            transform:
                translate(-50%, -50%)
                scale(1.06);

            background:
                rgba(124, 58, 237, 0.75);
        }


        /* =====================================================
           QUICK ACTIONS
           ===================================================== */

        .quick-actions {
            display: grid;

            grid-template-columns:
                repeat(4, minmax(0, 1fr));

            gap: 9px;

            padding: 12px;
        }


        .quick-card {
            min-width: 0;

            padding: 13px;

            border:
                1px solid
                rgba(255, 255, 255, 0.05);

            border-radius: 10px;

            background:
                rgba(255, 255, 255, 0.018);

            color: inherit;

            cursor: pointer;

            text-align: left;

            transition:
                transform .18s ease,
                background .18s ease,
                border-color .18s ease;
        }


        .quick-card:hover {
            transform: translateY(-2px);

            background:
                rgba(124, 58, 237, 0.07);

            border-color:
                rgba(139, 92, 246, 0.18);
        }


        .quick-icon {
            margin-bottom: 8px;

            color: #a78bfa;

            font-size: 16px;
        }


        .quick-title {
            color: #cbd5e1;

            font-size: 10px;

            font-weight: 750;
        }


        .quick-text {
            margin-top: 4px;

            color: #475569;

            font-size: 9px;

            line-height: 1.5;
        }


        /* =====================================================
           STORYBOARD
           ===================================================== */

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

            cursor: pointer;

            transition:
                transform .18s ease,
                border-color .18s ease;
        }


        .scene:hover {
            transform: translateY(-2px);

            border-color:
                rgba(139, 92, 246, 0.2);
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
           ===================================================== */

        .timeline {
            margin-top: 18px;

            padding-bottom: 18px;
        }


        .timeline-body {
            padding: 18px;
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

            cursor: pointer;

            transition:
                opacity .18s ease,
                transform .18s ease;
        }


        .timeline-clip:hover {
            opacity: .8;

            transform: translateY(-1px);
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
           PROJECT PANEL
           ===================================================== */

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

            color: #f1f5f9;

            overflow-wrap: anywhere;
        }


        .project-description {
            margin-top: 7px;

            color: #64748b;

            font-size: 12px;

            line-height: 1.6;

            overflow-wrap: anywhere;
        }


        .project-type {
            display: inline-flex;

            margin-top: 10px;

            padding:
                4px
                7px;

            border:
                1px solid
                rgba(139, 92, 246, 0.16);

            border-radius: 999px;

            color: #a78bfa;

            background:
                rgba(124, 58, 237, 0.07);

            font-size: 8px;

            font-weight: 750;

            text-transform: uppercase;

            letter-spacing: .8px;
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

            transition:
                width .35s ease;
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

            padding: 9px 0;

            cursor: pointer;
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

            flex: 0 0 23px;

            display: grid;
            place-items: center;

            border:
                1px solid
                rgba(255, 255, 255, 0.1);

            border-radius: 50%;

            background: #111827;

            color: #64748b;

            font-size: 9px;

            z-index: 1;

            transition:
                background .18s ease,
                color .18s ease,
                border-color .18s ease;
        }


        .workflow-step.active .step-dot {
            background: #7c3aed;

            border-color: #8b5cf6;

            color: white;

            box-shadow:
                0 0 16px
                rgba(124, 58, 237, 0.35);
        }


        .workflow-step.completed .step-dot {
            background:
                rgba(34, 197, 94, 0.12);

            border-color:
                rgba(34, 197, 94, 0.3);

            color: #86efac;
        }


        .step-name {
            color: #64748b;

            font-size: 12px;
        }


        .workflow-step.active .step-name {
            color: #fff;

            font-weight: 700;
        }


        .workflow-step.completed .step-name {
            color: #94a3b8;
        }


        .empty-project {
            padding: 14px;

            border:
                1px dashed
                rgba(255, 255, 255, 0.08);

            border-radius: 10px;

            color: #475569;

            font-size: 10px;

            line-height: 1.6;
        }


        /* =====================================================
           FEATURES
           ===================================================== */

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

            transition:
                transform .18s ease,
                border-color .18s ease;
        }


        .feature:hover {
            transform: translateY(-2px);

            border-color:
                rgba(139, 92, 246, 0.15);
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
           MODALS
           ===================================================== */

        .modal-backdrop {
            position: fixed;

            inset: 0;

            display: none;

            align-items: center;
            justify-content: center;

            padding: 20px;

            background:
                rgba(0, 0, 0, 0.72);

            backdrop-filter:
                blur(12px);

            z-index: 500;
        }


        .modal-backdrop.open {
            display: flex;
        }


        .modal {
            width: min(
                560px,
                100%
            );

            max-height:
                calc(100vh - 40px);

            overflow: auto;

            border:
                1px solid
                rgba(255, 255, 255, 0.08);

            border-radius: 18px;

            background:
                linear-gradient(
                    180deg,
                    #111522,
                    #0b0e16
                );

            box-shadow:
                0 40px 100px
                rgba(0, 0, 0, 0.5);
        }


        .modal-header {
            display: flex;

            align-items: center;

            justify-content: space-between;

            padding:
                18px
                20px;

            border-bottom:
                1px solid
                rgba(255, 255, 255, 0.06);
        }


        .modal-title {
            color: #f8fafc;

            font-size: 16px;

            font-weight: 800;
        }


        .modal-subtitle {
            main-top: 4px;

            color: #64748b;

            font-size: 10px;
        }


        .close-button {
            width: 32px;
            height: 32px;

            display: grid;
            place-items: center;

            border:
                1px solid
                rgba(255, 255, 255, 0.06);

            border-radius: 8px;

            background:
                rgba(255, 255, 255, 0.025);

            color: #94a3b8;

            cursor: pointer;
        }


        .close-button:hover {
            color: white;

            background:
                rgba(255, 255, 255, 0.07);
        }


        .modal-body {
            padding: 20px;
        }


        .form-group {
            margin-bottom: 15px;
        }


        .form-label {
            display: block;

            margin-bottom: 7px;

            text-align: left;

            color: #cbd5e1;

            font-size: 10px;

            font-weight: 750;
        }


        .form-input,
        .form-textarea,
        .form-select {
            width: 100%;

            border:
                1px solid
                rgba(255, 255, 255, 0.08);

            border-radius: 10px;

            outline: none;

            background:
                rgba(255, 255, 255, 0.035);

            color: #e2e8f0;

            transition:
                border-color .18s ease,
                background .18s ease;
        }


        .form-input,
        .form-select {
            height: 42px;

            padding:
                0
                12px;
        }


        .form-textarea {
            min-height: 110px;

            resize: vertical;

            padding: 11px 12px;

            line-height: 1.55;
        }


        .form-input:focus,
        .form-textarea:focus,
        .form-select:focus {
            border-color:
                rgba(139, 92, 246, 0.5);

            background:
                rgba(255, 255, 255, 0.05);
        }


        .form-select option {
            background: #111522;

            color: #e2e8f0;
        }


        .modal-actions {
            display: flex;

            justify-content: flex-end;

            gap: 9px;

            margin-top: 20px;
        }


        .projects-list {
            display: flex;

            flex-direction: column;

            gap: 9px;
        }


        .project-item {
            display: flex;

            align-items: center;

            justify-content: space-between;

            gap: 12px;

            padding: 13px;

            border:
                1px solid
                rgba(255, 255, 255, 0.06);

            border-radius: 11px;

            background:
                rgba(255, 255, 255, 0.02);
        }


        .project-item.current {
            border-color:
                rgba(139, 92, 246, 0.3);

            background:
                rgba(124, 58, 237, 0.07);
        }


        .project-item-info {
            min-width: 0;
        }


        .project-item-name {
            color: #e2e8f0;

            font-size: 12px;

            font-weight: 750;

            overflow-wrap: anywhere;
        }


        .project-item-description {
            margin-top: 4px;

            color: #64748b;

            font-size: 9px;

            line-height: 1.5;

            overflow-wrap: anywhere;
        }


        .project-item-type {
            margin-top: 5px;

            color: #7c8aa0;

            font-size: 8px;

            text-transform: uppercase;

            letter-spacing: .7px;
        }


        .project-open {
            flex: 0 0 auto;

            min-height: 32px;

            padding:
                0
                10px;

            border:
                1px solid
                rgba(255, 255, 255, 0.07);

            border-radius: 8px;

            background:
                rgba(255, 255, 255, 0.03);

            color: #cbd5e1;

            cursor: pointer;

            font-size: 9px;

            font-weight: 750;
        }


        .project-open:hover {
            background:
                rgba(124, 58, 237, 0.14);

            color: white;
        }


        /* =====================================================
           TOAST
           ===================================================== */

        .toast-container {
            position: fixed;

            right: 20px;
            bottom: 20px;

            display: flex;

            flex-direction: column;

            gap: 8px;

            z-index: 800;
        }


        .toast {
            min-width: 260px;

            max-width: 380px;

            padding:
                12px
                14px;

            border:
                1px solid
                rgba(255, 255, 255, 0.08);

            border-radius: 10px;

            background:
                rgba(15, 18, 28, 0.96);

            box-shadow:
                0 15px 40px
                rgba(0, 0, 0, 0.32);

            color: #cbd5e1;

            font-size: 10px;

            line-height: 1.5;

            animation:
                toastIn .22s ease;
        }


        .toast.success {
            border-color:
                rgba(34, 197, 94, 0.2);
        }


        .toast.error {
            border-color:
                rgba(239, 68, 68, 0.25);
        }


        .toast-title {
            color: #f8fafc;

            font-size: 10px;

            font-weight: 800;

            margin-bottom: 2px;
        }


        @keyframes toastIn {

            from {
                opacity: 0;
                transform: translateY(10px);
            }

            to {
                opacity: 1;
                transform: translateY(0);
            }

        }


        /* =====================================================
           MOBILE
           ===================================================== */

        @media (max-width: 1100px) {

            .app {
                grid-template-columns:
                    215px
                    minmax(0, 1fr);
            }


            .sidebar {
                width: 215px;
            }


            .main {
                margin-left: 215px;
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
                width: 250px;

                transform:
                    translateX(-100%);

                transition:
                    transform .25s ease;

                box-shadow:
                    20px 0 60px
                    rgba(0, 0, 0, 0.4);
            }


            .sidebar.open {
                transform:
                    translateX(0);
            }


            .main {
                margin-left: 0;

                padding:
                    0
                    16px
                    40px;
            }


            .mobile-menu {
                data-display: grid;
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


            .topbar {
                height: 64px;
            }


            .breadcrumb {
                display: none;
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


            .topbar-actions {
                gap: 5px;
            }


            .top-button.docs-button {
                display: none;
            }


            .hero-actions {
                flex-direction: column;
            }


            .primary-button,
            .secondary-button {
                width: 100%;
            }


            .toast-container {
                left: 14px;
                right: 14px;
                bottom: 14px;
            }


            .toast {
                min-width: 0;

                width: 100%;
            }

        }

    </style>

</head>


<body>


<div class="app">


    <!-- =====================================================
         SIDEBAR
         ===================================================== -->

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

                <div class="brand-subtitle" data-i18n="brand_subtitle">
                    Creative OS
                </div>

            </div>

        </div>


        <div class="nav-section">

            <div class="nav-label" data-i18n="nav_create">
                Create
            </div>


            <button
                class="nav-item active"
                data-module="new"
                onclick="startFilm()"
            >

                <div class="nav-icon">
                    ✦
                </div>

                <div class="nav-text" data-i18n="nav_new_film">
                    New Film
                </div>

            </button>


            <button
                class="nav-item"
                data-module="projects"
                onclick="openProjects()"
            >

                <div class="nav-icon">
                    ▦
                </div>

                <div class="nav-text" data-i18n="nav_projects">
                    Projects
                </div>

            </button>

        </div>


        <div class="nav-section">

            <div class="nav-label" data-i18n="nav_story">
                Story
            </div>


            <button
                class="nav-item"
                data-module="script"
                onclick="openModule('script', 1)"
            >

                <div class="nav-icon">
                    ≡
                </div>

                <div class="nav-text" data-i18n="nav_script">
                    Script
                </div>

            </button>


            <button
                class="nav-item"
                data-module="characters"
                onclick="openModule('characters', 2)"
            >

                <div class="nav-icon">
                    ◉
                </div>

                <div class="nav-text" data-i18n="nav_characters">
                    Characters
                </div>

            </button>


            <button
                class="nav-item"
                data-module="storyboard"
                onclick="openModule('storyboard', 3)"
            >

                <div class="nav-icon">
                    ▤
                </div>

                <div class="nav-text" data-i18n="nav_storyboard">
                    Storyboard
                </div>

            </button>


            <button
                class="nav-item"
                data-module="scenes"
                onclick="openModule('scenes', 4)"
            >

                <div class="nav-icon">
                    ◇
                </div>

                <div class="nav-text" data-i18n="nav_scenes">
                    Scenes
                </div>

            </button>

        </div>


        <div class="nav-section">

            <div class="nav-label" data-i18n="nav_production">
                Production
            </div>


            <button
                class="nav-item"
                data-module="video"
                onclick="openModule('video', 5)"
            >

                <div class="nav-icon">
                    ▶
                </div>

                <div class="nav-text" data-i18n="nav_video">
                    Video
                </div>

            </button>


            <button
                class="nav-item"
                data-module="voice"
                onclick="openModule('voice', 6)"
            >

                <div class="nav-icon">
                    ♫
                </div>

                <div class="nav-text" data-i18n="nav_voice">
                    Voice
                </div>

            </button>


            <button
                class="nav-item"
                data-module="music"
                onclick="openModule('music', 7)"
            >

                <div class="nav-icon">
                    ♪
                </div>

                <div class="nav-text" data-i18n="nav_music">
                    Music
                </div>

            </button>

        </div>


        <div class="nav-section">

            <div class="nav-label" data-i18n="nav_localize">
                Localize
            </div>


            <button
                class="nav-item"
                data-module="languages"
                onclick="openModule('languages', 8)"
            >

                <div class="nav-icon">
                    文
                </div>

                <div class="nav-text" data-i18n="nav_languages">
                    Languages
                </div>

            </button>


            <button
                class="nav-item"
                data-module="dubbing"
                onclick="openModule('dubbing', 8)"
            >

                <div class="nav-icon">
                    ◎
                </div>

                <div class="nav-text" data-i18n="nav_dubbing">
                    Dubbing
                </div>

            </button>


            <button
                class="nav-item"
                data-module="subtitles"
                onclick="openModule('subtitles', 8)"
            >

                <div class="nav-icon">
                    Aa
                </div>

                <div class="nav-text" data-i18n="nav_subtitles">
                    Subtitles
                </div>

            </button>

        </div>


        <div class="nav-section">

            <div class="nav-label" data-i18n="nav_export">
                Export
            </div>


            <button
                class="nav-item"
                data-module="render"
                onclick="openModule('render', 9)"
            >

                <div class="nav-icon">
                    ◆
                </div>

                <div class="nav-text" data-i18n="nav_render">
                    Render Film
                </div>

            </button>

        </div>


        <div class="sidebar-spacer"></div>


        <div class="system-status">

            <div class="system-status-row">

                <div class="status-dot"></div>

                <span data-i18n="system_status_online">
                    ACOS Core Online
                </span>

            </div>

            <div class="system-version">
                CreativeOS v0.3
            </div>

        </div>


    </aside>


    <!-- =====================================================
         MAIN
         ===================================================== -->

    <main class="main">


        <!-- TOPBAR -->

        <header class="topbar">


            <div class="topbar-left">


                <button
                    class="top-button mobile-menu"
                    onclick="toggleSidebar()"
                    aria-label="Open menu"
                >
                    ☰
                </button>


                <div class="breadcrumb">

                    ACOS

                    <span>
                        /
                    </span>

                    <strong data-i18n="breadcrumb_studio">
                        Studio
                    </strong>

                </div>

            </div>


            <div class="topbar-actions">

                <!-- Language Selector -->
                <div class="language-select-wrapper">
                    <select id="languageSelect" class="language-select" onchange="changeLanguage(this.value)" aria-label="Language selector">
                        <option value="en">English</option>
                    </select>
                </div>


                <button
                    class="top-button docs-button"
                    onclick="openDocs()"
                    title="Open API documentation"
                >
                    ?
                    <span data-i18n="docs_label">
                        Docs
                    </span>
                </button>


                <button
                    class="top-button health-button"
                    onclick="openHealth()"
                    title="Check ACOS health"
                >
                    ●
                    <span data-i18n="health_label">
                        Health
                    </span>
                </button>


                <div class="avatar">
                    A
                </div>

            </div>


        </header>


        <!-- HERO -->

        <section class="hero">


            <div class="hero-eyebrow" data-i18n="hero_eyebrow">
                ✦ AI Creative Operating System
            </div>


            <h1 data-i18n-html="hero_title">
                Create a film
                <span>
                    from imagination.
                </span>
            </h1>


            <p data-i18n="hero_description">
                Build stories, characters, scenes, video,
                voice, music and multilingual versions
                inside one cinematic creative workspace.
            </p>


            <div class="hero-actions">


                <button
                    class="primary-button"
                    onclick="startFilm()"
                    data-i18n-html="hero_create_btn"
                >
                    ✦
                    Create New Film
                </button>


                <button
                    class="secondary-button"
                    onclick="importScript()"
                    data-i18n-html="hero_import_btn"
                >
                    ↑
                    Import Script
                </button>


            </div>


        </section>


        <!-- WORKSPACE -->

        <section class="workspace">


            <!-- LEFT -->

            <div>


                <!-- PREVIEW -->

                <div class="panel preview">


                    <div class="panel-header">

                        <div class="panel-title" data-i18n="preview_title">
                            Film Preview
                        </div>

                        <div class="panel-label">
                            16:9 • Cinematic
                        </div>

                    </div>


                    <div class="preview-screen">


                        <div class="preview-empty">

                            <div class="preview-empty-icon">
                                ▶
                            </div>

                            <div class="preview-empty-title" data-i18n="preview_empty_title">
                                No generated film yet
                            </div>

                            <div class="preview-empty-text" data-i18n="preview_empty_text">
                                Create a project and begin your story.
                            </div>

                        </div>


                        <button
                            class="preview-play"
                            onclick="previewFilm()"
                            aria-label="Preview film"
                        >
                            ▶
                        </button>


                    </div>


                    <!-- QUICK ACTIONS -->

                    <div class="quick-actions">


                        <button
                            class="quick-card"
                            onclick="quickAction('script')"
                        >

                            <div class="quick-icon">
                                ≡
                            </div>

                            <div class="quick-title" data-i18n="quick_script_title">
                                Write Script
                            </div>

                            <div class="quick-text" data-i18n="quick_script_text">
                                Turn your idea into a screenplay.
                            </div>

                        </button>


                        <button
                            class="quick-card"
                            onclick="quickAction('characters')"
                        >

                            <div class="quick-icon">
                                ◉
                            </div>

                            <div class="quick-title" data-i18n="quick_char_title">
                                Build Characters
                            </div>

                            <div class="quick-text" data-i18n="quick_char_text">
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

                            <div class="quick-title" data-i18n="quick_storyboard_title">
                                Storyboard
                            </div>

                            <div class="quick-text" data-i18n="quick_storyboard_text">
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

                            <div class="quick-title" data-i18n="quick_video_title">
                                Generate Video
                            </div>

                            <div class="quick-text" data-i18n="quick_video_text">
                                Turn scenes into cinematic video.
                            </div>

                        </button>


                    </div>

                </div>


                <!-- STORYBOARD -->

                <div class="panel storyboard">


                    <div class="panel-header">

                        <div class="panel-title" data-i18n="storyboard_panel_title">
                            Storyboard
                        </div>

                        <div
                            class="panel-label"
                            id="sceneCount"
                        >
                            4 scenes
                        </div>

                    </div>


                    <div class="scene-grid">


                        <div
                            class="scene"
                            onclick="openModule('storyboard', 3)"
                        >

                            <div class="scene-image" data-i18n="scene_preview_label">
                                Scene preview
                            </div>

                            <div class="scene-info">

                                <div class="scene-number" data-i18n="scene_01">
                                    Scene 01
                                </div>

                                <div class="scene-name" data-i18n="scene_opening">
                                    Opening
                                </div>

                            </div>

                        </div>


                        <div
                            class="scene"
                            onclick="openModule('storyboard', 3)"
                        >

                            <div class="scene-image" data-i18n="scene_preview_label">
                                Scene preview
                            </div>

                            <div class="scene-info">

                                <div class="scene-number" data-i18n="scene_02">
                                    Scene 02
                                </div>

                                <div class="scene-name" data-i18n="scene_encounter">
                                    The Encounter
                                </div>

                            </div>

                        </div>


                        <div
                            class="scene"
                            onclick="openModule('storyboard', 3)"
                        >

                            <div class="scene-image" data-i18n="scene_preview_label">
                                Scene preview
                            </div>

                            <div class="scene-info">

                                <div class="scene-number" data-i18n="scene_03">
                                    Scene 03
                                </div>

                                <div class="scene-name" data-i18n="scene_conflict">
                                    The Conflict
                                </div>

                            </div>

                        </div>


                        <div
                            class="scene"
                            onclick="openModule('storyboard', 3)"
                        >

                            <div class="scene-image" data-i18n="scene_preview_label">
                                Scene preview
                            </div>

                            <div class="scene-info">

                                <div class="scene-number" data-i18n="scene_04">
                                    Scene 04
                                </div>

                                <div class="scene-name" data-i18n="scene_resolution">
                                    Resolution
                                </div>

                            </div>

                        </div>


                    </div>

                </div>


                <!-- TIMELINE -->

                <div class="panel timeline">


                    <div class="panel-header">

                        <div class="panel-title" data-i18n="timeline_title">
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
                                onclick="openModule('scenes', 4)"
                            ></div>


                            <div
                                class="timeline-clip clip-two"
                                onclick="openModule('scenes', 4)"
                            ></div>


                            <div
                                class="timeline-clip clip-three"
                                onclick="openModule('scenes', 4)"
                            ></div>


                            <div
                                class="timeline-clip clip-four"
                                onclick="openModule('scenes', 4)"
                            ></div>


                        </div>

                    </div>

                </div>


            </div>


            <!-- RIGHT / PROJECT -->

            <aside>


                <div class="panel project-panel">


                    <div class="panel-header">

                        <div class="panel-title" data-i18n="current_film_title">
                            Current Film
                        </div>

                        <div
                            class="panel-label"
                            id="projectStatusLabel"
                            data-i18n="status_draft"
                        >
                            Draft
                        </div>

                    </div>


                    <div class="project-content">


                        <div
                            class="project-title"
                            id="currentProjectTitle"
                            data-i18n="no_film_selected"
                        >
                            No film selected
                        </div>


                        <div
                            class="project-description"
                            id="currentProjectDescription"
                            data-i18n="no_film_desc"
                        >
                            Create a new film project and begin
                            building your production step by step.
                        </div>


                        <div
                            class="project-type"
                            id="currentProjectType"
                            style="display:none;"
                        >
                            Film
                        </div>


                        <div class="progress">

                            <div
                                class="progress-bar"
                                id="progressBar"
                            ></div>

                        </div>


                        <div class="workflow">


                            <div
                                class="workflow-step active"
                                data-step="0"
                                onclick="activateStep(0)"
                            >

                                <div class="step-dot">
                                    1
                                </div>

                                <div class="step-name" data-i18n="wf_step_0">
                                    Idea
                                </div>

                            </div>


                            <div
                                class="workflow-step"
                                data-step="1"
                                onclick="activateStep(1)"
                            >

                                <div class="step-dot">
                                    2
                                </div>

                                <div class="step-name" data-i18n="wf_step_1">
                                    Script
                                </div>

                            </div>


                            <div
                                class="workflow-step"
                                data-step="2"
                                onclick="activateStep(2)"
                            >

                                <div class="step-dot">
                                    3
                                </div>

                                <div class="step-name" data-i18n="wf_step_2">
                                    Characters
                                </div>

                            </div>


                            <div
                                class="workflow-step"
                                data-step="3"
                                onclick="activateStep(3)"
                            >

                                <div class="step-dot">
                                    4
                                </div>

                                <div class="step-name" data-i18n="wf_step_3">
                                    Storyboard
                                </div>

                            </div>


                            <div
                                class="workflow-step"
                                data-step="4"
                                onclick="activateStep(4)"
                            >

                                <div class="step-dot">
                                    5
                                </div>

                                <div class="step-name" data-i18n="wf_step_4">
                                    Scenes
                                </div>

                            </div>


                            <div
                                class="workflow-step"
                                data-step="5"
                                onclick="activateStep(5)"
                            >

                                <div class="step-dot">
                                    6
                                </div>

                                <div class="step-name" data-i18n="wf_step_5">
                                    Video
                                </div>

                            </div>


                            <div
                                class="workflow-step"
                                data-step="6"
                                onclick="activateStep(6)"
                            >

                                <div class="step-dot">
                                    7
                                </div>

                                <div class="step-name" data-i18n="wf_step_6">
                                    Voice
                                </div>

                            </div>


                            <div
                                class="workflow-step"
                                data-step="7"
                                onclick="activateStep(7)"
                            >

                                <div class="step-dot">
                                    8
                                </div>

                                <div class="step-name" data-i18n="wf_step_7">
                                    Music
                                </div>

                            </div>


                            <div
                                class="workflow-step"
                                data-step="8"
                                onclick="activateStep(8)"
                            >

                                <div class="step-dot">
                                    9
                                </div>

                                <div class="step-name" data-i18n="wf_step_8">
                                    Translation
                                </div>

                            </div>


                            <div
                                class="workflow-step"
                                data-step="9"
                                onclick="activateStep(9)"
                            >

                                <div class="step-dot">
                                    10
                                </div>

                                <div class="step-name" data-i18n="wf_step_9">
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

                <h3 data-i18n="feat_1_title">
                    Film Creation
                </h3>

                <p data-i18n="feat_1_text">
                    Build an entire production from
                    concept to final film inside one workspace.
                </p>

            </div>


            <div class="feature">

                <div class="feature-icon">
                    🧠
                </div>

                <h3 data-i18n="feat_2_title">
                    AI Creative Engine
                </h3>

                <p data-i18n="feat_2_text">
                    Connect multiple AI providers for
                    generation, analysis and quality control.
                </p>

            </div>


            <div class="feature">

                <div class="feature-icon">
                    🌍
                </div>

                <h3 data-i18n="feat_3_title">
                    Global Localization
                </h3>

                <p data-i18n="feat_3_text">
                    Translate, dub and subtitle films
                    for audiences around the world.
                </p>

            </div>


        </section>


    </main>

</div>


<!-- =========================================================
     NEW FILM MODAL
     ========================================================= -->

<div
    class="modal-backdrop"
    id="newFilmModal"
    onclick="backdropClose(event, 'newFilmModal')"
>


    <div class="modal">


        <div class="modal-header">


            <div>

                <div class="modal-title" data-i18n="modal_new_film_title">
                    Create New Film
                </div>

                <div class="modal-subtitle" data-i18n="modal_new_film_sub">
                    Start a new ACOS creative project.
                </div>

            </div>


            <button
                class="close-button"
                onclick="closeModal('newFilmModal')"
                aria-label="Close"
            >
                ×
            </button>


        </div>


        <form
            class="modal-body"
            onsubmit="createFilm(event)"
        >


            <div class="form-group">

                <label
                    class="form-label"
                    for="filmName"
                    data-i18n="label_film_name"
                >
                    Film name
                </label>

                <input
                    id="filmName"
                    class="form-input"
                    type="text"
                    maxlength="200"
                    placeholder="e.g. The Last Horizon"
                    required
                >

            </div>


            <div class="form-group">

                <label
                    class="form-label"
                    for="filmDescription"
                    data-i18n="label_description"
                >
                    Description
                </label>

                <textarea
                    id="filmDescription"
                    class="form-textarea"
                    maxlength="2000"
                    placeholder="Describe the idea, story or creative direction..."
                ></textarea>

            </div>


            <div class="form-group">

                <label
                    class="form-label"
                    for="filmType"
                    data-i18n="label_project_type"
                >
                    Project type
                </label>

                <select
                    id="filmType"
                    class="form-select"
                >

                    <option value="film" data-i18n="opt_film">
                        Film
                    </option>

                    <option value="short_film" data-i18n="opt_short_film">
                        Short Film
                    </option>

                    <option value="series" data-i18n="opt_series">
                        Series
                    </option>

                    <option value="animation" data-i18n="opt_animation">
                        Animation
                    </option>

                </select>

            </div>


            <div class="modal-actions">


                <button
                    type="button"
                    class="secondary-button"
                    onclick="closeModal('newFilmModal')"
                    data-i18n="btn_cancel"
                >
                    Cancel
                </button>


                <button
                    type="submit"
                    class="primary-button"
                    id="createFilmButton"
                    data-i18n-html="btn_create_film"
                >
                    ✦
                    Create Film
                </button>


            </div>


        </form>


    </div>

</div>


<!-- =========================================================
     PROJECTS MODAL
     ========================================================= -->

<div
    class="modal-backdrop"
    id="projectsModal"
    onclick="backdropClose(event, 'projectsModal')"
>


    <div class="modal">


        <div class="modal-header">


            <div>

                <div class="modal-title" data-i18n="modal_projects_title">
                    Projects
                </div>

                <div class="modal-subtitle" data-i18n="modal_projects_sub">
                    Select an existing ACOS film project.
                </div>

            </div>


            <button
                class="close-button"
                onclick="closeModal('projectsModal')"
                aria-label="Close"
            >
                ×
            </button>


        </div>


        <div class="modal-body">


            <div
                class="projects-list"
                id="projectsList"
            >

                <div class="empty-project" data-i18n="loading_projects">
                    Loading projects...
                </div>

            </div>


            <div class="modal-actions">


                <button
                    class="primary-button"
                    onclick="closeModal('projectsModal'); startFilm();"
                    data-i18n-html="btn_new_film_modal"
                >
                    ✦
                    New Film
                </button>


            </div>


        </div>


    </div>

</div>


<!-- =========================================================
     IMPORT SCRIPT MODAL
     ========================================================= -->

<div
    class="modal-backdrop"
    id="importModal"
    onclick="backdropClose(event, 'importModal')"
>


    <div class="modal">


        <div class="modal-header">


            <div>

                <div class="modal-title" data-i18n="modal_import_title">
                    Import Script
                </div>

                <div class="modal-subtitle" data-i18n="modal_import_sub">
                    Load a text-based screenplay into the Studio.
                </div>

            </div>


            <button
                class="close-button"
                onclick="closeModal('importModal')"
                aria-label="Close"
            >
                ×
            </button>


        </div>


        <div class="modal-body">


            <div class="form-group">

                <label
                    class="form-label"
                    for="scriptFile"
                    data-i18n="label_script_file"
                >
                    Script file
                </label>

                <input
                    id="scriptFile"
                    class="form-input"
                    type="file"
                    accept=".txt,.md,.fdx"
                    onchange="handleScriptFile(event)"
                >

            </div>


            <div
                id="importInfo"
                class="empty-project"
                data-i18n="import_supported_formats"
            >
                Supported formats:
                TXT, Markdown and Final Draft XML.
                The selected file will be read locally in your browser.
            </div>


            <div class="modal-actions">


                <button
                    class="secondary-button"
                    onclick="closeModal('importModal')"
                    data-i18n="btn_close"
                >
                    Close
                </button>


                <button
                    class="primary-button"
                    onclick="processImportedScript()"
                    data-i18n="btn_continue"
                >
                    Continue
                </button>


            </div>


        </div>


    </div>

</div>


<!-- =========================================================
     TOAST CONTAINER
     ========================================================= -->

<div
    class="toast-container"
    id="toastContainer"
></div>


<script>

    /*
     * ========================================================
     * ACOS CLIENT STATE & LOCALIZATION
     * ========================================================
     */

    let projects = [];
    let currentProject = null;
    let currentStep = 0;
    let importedScriptText = "";
    let currentTranslations = {};

    const DEFAULT_LANGUAGE = "en";

    // 15 Required Languages List
    const SUPPORTED_LANGUAGES = [
        { code: "hy", name: "Հայերեն" },
        { code: "en", name: "English" },
        { code: "ru", name: "Русский" },
        { code: "zh", name: "中文" },
        { code: "hi", name: "हिन्दी" },
        { code: "es", name: "Español" },
        { code: "ar", name: "العربية" },
        { code: "fr", name: "Français" },
        { code: "bn", name: "বাংলা" },
        { code: "pt", name: "Português" },
        { code: "id", name: "Bahasa Indonesia" },
        { code: "ur", name: "اردو" },
        { code: "de", name: "Deutsch" },
        { code: "ja", name: "日本語" },
        { code: "pcm", name: "Nigerian Pidgin" }
    ];


    const workflowNames = [
        "Idea",
        "Script",
        "Characters",
        "Storyboard",
        "Scenes",
        "Video",
        "Voice",
        "Music",
        "Translation",
        "Final Film"
    ];


    /*
     * ========================================================
     * INTERNATIONALIZATION (i18n) LOGIC
     * ========================================================
     */

    async function initLanguageSystem() {
        const selectEl = document.getElementById("languageSelect");
        if (selectEl) {
            selectEl.innerHTML = SUPPORTED_LANGUAGES.map(lang => 
                `<option value="${lang.code}">${lang.name}</option>`
            ).join("");
        }

        const savedLanguage = localStorage.getItem("acos_language") || DEFAULT_LANGUAGE;
        if (selectEl) {
            selectEl.value = savedLanguage;
        }

        await loadAndApplyLanguage(savedLanguage);
    }

    async function changeLanguage(languageCode) {
        localStorage.setItem("acos_language", languageCode);
        await loadAndApplyLanguage(languageCode);
    }

    async function loadAndApplyLanguage(languageCode) {
        // RTL adjustment for Arabic and Urdu
        document.documentElement.dir = (languageCode === "ar" || languageCode === "ur") ? "rtl" : "ltr";
        document.documentElement.lang = languageCode;

        try {
            await apiRequest("/api/i18n/languages").catch(() => {});
            const data = await apiRequest(`/api/i18n/ui/${languageCode}`);
            currentTranslations = (data && typeof data === "object") ? (data.translations || data) : {};
        } catch (error) {
            console.warn("Could not fetch translations from API, using fallback context:", error);
            currentTranslations = {};
        }

        applyTranslationsToDOM();
    }

    function applyTranslationsToDOM() {
        document.querySelectorAll("[data-i18n]").forEach(el => {
            const key = el.getAttribute("data-i18n");
            if (currentTranslations[key]) {
                el.textContent = currentTranslations[key];
            }
        });

        document.querySelectorAll("[data-i18n-html]").forEach(el => {
            const key = el.getAttribute("data-i18n-html");
            if (currentTranslations[key]) {
                el.innerHTML = currentTranslations[key];
            }
        });
    }


    /*
     * ========================================================
     * BASIC UI
     * ========================================================
     */

    function toggleSidebar() {

        const sidebar =
            document.getElementById("sidebar");

        sidebar.classList.toggle("open");
    }


    function closeSidebarOnMobile() {

        if (window.innerWidth <= 800) {

            const sidebar =
                document.getElementById("sidebar");

            sidebar.classList.remove("open");
        }
    }


    function selectNav(element) {

        document
            .querySelectorAll(".nav-item")
            .forEach(
                item => item.classList.remove("active")
            );

        if (element) {

            element.classList.add("active");
        }

        closeSidebarOnMobile();
    }


    function activateNav(moduleName) {

        document
            .querySelectorAll(".nav-item")
            .forEach(item => {

                item.classList.toggle(
                    "active",
                    item.dataset.module === moduleName
                );

            });

        closeSidebarOnMobile();
    }


    /*
     * ========================================================
     * MODALS
     * ========================================================
     */

    function openModal(id) {

        const modal =
            document.getElementById(id);

        if (!modal) {
            return;
        }

        modal.classList.add("open");

        document.body.style.overflow = "hidden";
    }


    function closeModal(id) {

        const modal =
            document.getElementById(id);

        if (!modal) {
            return;
        }

        modal.classList.remove("open");

        const anyOpen =
            document.querySelector(
                ".modal-backdrop.open"
            );

        if (!anyOpen) {

            document.body.style.overflow = "";
        }
    }


    function backdropClose(event, id) {

        if (
            event.target ===
            document.getElementById(id)
        ) {

            closeModal(id);
        }
    }


    /*
     * ========================================================
     * TOAST
     * ========================================================
     */

    function showToast(
        message,
        type = "success",
        title = ""
    ) {

        const container =
            document.getElementById(
                "toastContainer"
            );

        const toast =
            document.createElement("div");

        toast.className =
            "toast " + type;

        const titleHtml =
            title
                ? '<div class="toast-title">' +
                  escapeHtml(title) +
                  '</div>'
                : "";

        toast.innerHTML =
            titleHtml +
            '<div>' +
            escapeHtml(message) +
            '</div>';

        container.appendChild(toast);

        window.setTimeout(
            function () {

                toast.style.opacity = "0";

                toast.style.transform =
                    "translateY(8px)";

                window.setTimeout(
                    function () {

                        toast.remove();

                    },
                    220
                );

            },
            3500
        );
    }


    /*
     * ========================================================
     * SAFE HTML
     * ========================================================
     */

    function escapeHtml(value) {

        return String(value ?? "")
            .replaceAll("&", "&amp;")
            .replaceAll("<", "&lt;")
            .replaceAll(">", "&gt;")
            .replaceAll('"', "&quot;")
            .replaceAll("'", "&#039;");
    }


    /*
     * ========================================================
     * API HELPERS
     * ========================================================
     */

    async function apiRequest(
        url,
        options = {}
    ) {

        const response =
            await fetch(
                url,
                {
                    ...options,

                    headers: {
                        "Accept":
                            "application/json",

                        ...(options.body
                            ? {
                                "Content-Type":
                                    "application/json"
                            }
                            : {}),

                        ...(options.headers || {})
                    }
                }
            );

        let data = null;

        const contentType =
            response.headers.get(
                "content-type"
            ) || "";

        if (
            contentType.includes(
                "application/json"
            )
        ) {

            data =
                await response.json();

        } else {

            data =
                await response.text();
        }


        if (!response.ok) {

            let message =
                "API request failed.";

            if (
                data &&
                typeof data === "object"
            ) {

                if (
                    typeof data.detail === "string"
                ) {

                    message =
                        data.detail;

                } else {

                    try {

                        message =
                            JSON.stringify(
                                data
                            );

                    } catch (error) {

                        message =
                            "API request failed.";
                    }
                }

            } else if (data) {

                message =
                    String(data);
            }


            const error =
                new Error(message);

            error.status =
                response.status;

            error.data =
                data;

            throw error;
        }


        return data;
    }


    /*
     * ========================================================
     * PROJECT NORMALIZATION
     * ========================================================
     */

    function normalizeProject(
        project,
        index
    ) {

        const safe =
            project &&
            typeof project === "object"
                ? project
                : {};

        return {

            id:
                safe.id ??
                safe.project_id ??
                ("local-" + index),

            name:
                safe.name ||
                "Untitled Film",

            description:
                safe.description ||
                "No description yet.",

            project_type:
                safe.project_type ||
                "film"

        };
    }


    /*
     * ========================================================
     * LOAD PROJECTS
     * ========================================================
     */

    async function loadProjects(
        autoSelect = true
    ) {

        try {

            const data =
                await apiRequest(
                    "/api/projects"
                );


            const rawProjects =
                Array.isArray(data)
                    ? data
                    : [];


            projects =
                rawProjects.map(
                    normalizeProject
                );


            renderProjects();


            if (
                autoSelect &&
                projects.length > 0
            ) {

                if (!currentProject) {

                    setCurrentProject(
                        projects[0],
                        false
                    );

                } else {

                    const existing =
                        projects.find(
                            project =>
                                String(project.id) ===
                                String(
                                    currentProject.id
                                )
                        );

                    if (existing) {

                        setCurrentProject(
                            existing,
                            false
                        );

                    } else {

                        setCurrentProject(
                            projects[0],
                            false
                        );
                    }
                }

            } else if (
                projects.length === 0
            ) {

                setEmptyProjectState();
            }


        } catch (error) {

            console.error(
                "Failed to load projects:",
                error
            );


            projects = [];


            renderProjects(
                "Unable to load projects."
            );


            showToast(
                error.message ||
                "Could not load projects.",
                "error",
                "Projects"
            );
        }
    }


    /*
     * ========================================================
     * RENDER PROJECT LIST
     * ========================================================
     */

    function renderProjects(
        emptyMessage = ""
    ) {

        const container =
            document.getElementById(
                "projectsList"
            );


        if (!container) {
            return;
        }


        if (!projects.length) {

            container.innerHTML =
                '<div class="empty-project">' +
                escapeHtml(
                    emptyMessage ||
                    "No film projects yet. Create your first project."
                ) +
                "</div>";

            return;
        }


        container.innerHTML =
            projects
                .map(
                    function (project) {

                        const isCurrent =
                            currentProject &&
                            String(
                                currentProject.id
                            ) ===
                            String(
                                project.id
                            );


                        return `
                            <div
                                class="project-item ${
                                    isCurrent
                                        ? "current"
                                        : ""
                                }"
                            >

                                <div class="project-item-info">

                                    <div class="project-item-name">
                                        ${escapeHtml(project.name)}
                                    </div>

                                    <div class="project-item-description">
                                        ${escapeHtml(project.description)}
                                    </div>

                                    <div class="project-item-type">
                                        ${escapeHtml(project.project_type)}
                                    </div>

                                </div>

                                <button
                                    class="project-open"
                                    onclick="selectProjectById(${JSON.stringify(String(project.id))})"
                                >
                                    ${
                                        isCurrent
                                            ? "Current"
                                            : "Open"
                                    }
                                </button>

                            </div>
                        `;
                    }
                )
                .join("");
    }


    /*
     * ========================================================
     * SELECT PROJECT
     * ========================================================
     */

    function selectProjectById(
        id
    ) {

        const project =
            projects.find(
                item =>
                    String(item.id) ===
                    String(id)
            );


        if (!project) {

            showToast(
                "The selected project could not be found.",
                "error",
                "Project"
            );

            return;
        }


        setCurrentProject(
            project,
            true
        );
    }


    function setCurrentProject(
        project,
        closeProjects = true
    ) {

        currentProject =
            project;


        const title =
            document.getElementById(
                "currentProjectTitle"
            );

        const description =
            document.getElementById(
                "currentProjectDescription"
            );

        const type =
            document.getElementById(
                "currentProjectType"
            );


        if (title) {

            title.textContent =
                project.name;
        }


        if (description) {

            description.textContent =
                project.description;
        }


        if (type) {

            type.textContent =
                project.project_type;

            type.style.display =
                "inline-flex";
        }


        const status =
            document.getElementById(
                "projectStatusLabel"
            );


        if (status) {

            status.textContent =
                "Draft";
        }


        activateStep(
            0,
            false
        );


        renderProjects();


        if (closeProjects) {

            closeModal(
                "projectsModal"
            );


            showToast(
                project.name +
                " is now the current film.",
                "success",
                "Project selected"
            );
        }
    }


    function setEmptyProjectState() {

        currentProject = null;


        const title =
            document.getElementById(
                "currentProjectTitle"
            );

        const description =
            document.getElementById(
                "currentProjectDescription"
            );

        const type =
            document.getElementById(
                "currentProjectType"
            );


        if (title) {

            title.textContent =
                "No film selected";
        }


        if (description) {

            description.textContent =
                "Create a new film project and begin building your production step by step.";
        }


        if (type) {

            type.style.display =
                "none";
        }


        activateStep(
            0,
            false
        );
    }


    /*
     * ========================================================
     * NEW FILM
     * ========================================================
     */

    function startFilm() {

        activateNav("new");


        const nameInput =
            document.getElementById(
                "filmName"
            );

        const descriptionInput =
            document.getElementById(
                "filmDescription"
            );


        if (nameInput) {

            nameInput.value = "";
        }


        if (descriptionInput) {

            descriptionInput.value = "";
        }


        openModal(
            "newFilmModal"
        );


        window.setTimeout(
            function () {

                if (nameInput) {

                    nameInput.focus();
                }

            },
            100
        );
    }


    async function createFilm(
        event
    ) {

        event.preventDefault();


        const nameInput =
            document.getElementById(
                "filmName"
            );

        const descriptionInput =
            document.getElementById(
                "filmDescription"
            );

        const typeInput =
            document.getElementById(
                "filmType"
            );

        const button =
            document.getElementById(
                "createFilmButton"
            );


        const name =
            nameInput.value.trim();


        const description =
            descriptionInput.value.trim();


        const projectType =
            typeInput.value.trim() ||
            "film";


        if (!name) {

            showToast(
                "Please enter a film name.",
                "error",
                "Create Film"
            );

            nameInput.focus();

            return;
        }


        button.disabled = true;

        button.style.opacity =
            "0.6";


        try {

            const project =
                await apiRequest(
                    "/api/projects",
                    {
                        method: "POST",

                        body: JSON.stringify(
                            {
                                name:
                                    name,

                                description:
                                    description ||
                                    "New ACOS film project.",

                                project_type:
                                    projectType
                            }
                        )
                    }
                );


            const normalized =
                normalizeProject(
                    project,
                    projects.length
                );


            projects.unshift(
                normalized
            );


            setCurrentProject(
                normalized,
                false
            );


            closeModal(
                "newFilmModal"
            );


            renderProjects();


            showToast(
                "Your film project has been created successfully.",
                "success",
                "Film created"
            );


            activateNav(
                "new"
            );


            await loadProjects(
                false
            );


        } catch (error) {

            console.error(
                "Create project error:",
                error
            );


            showToast(
                error.message ||
                "Could not create the film project.",
                "error",
                "Create Film"
            );

        } finally {

            button.disabled = false;

            button.style.opacity =
                "";
        }
    }


    /*
     * ========================================================
     * PROJECTS
     * ========================================================
     */

    async function openProjects() {

        activateNav(
            "projects"
        );


        openModal(
            "projectsModal"
        );


        await loadProjects(
            false
        );
    }


    /*
     * ========================================================
     * WORKFLOW
     * ========================================================
     */

    function activateStep(
        index,
        notify = true
    ) {

        const maxIndex =
            workflowNames.length - 1;


        currentStep =
            Math.max(
                0,
                Math.min(
                    index,
                    maxIndex
                )
            );


        const steps =
            document.querySelectorAll(
                ".workflow-step"
            );


        steps.forEach(
            function (
                step,
                stepIndex
            ) {

                step.classList.toggle(
                    "active",
                    stepIndex === currentStep
                );


                step.classList.toggle(
                    "completed",
                    stepIndex < currentStep
                );

            }
        );


        const progress =
            Math.max(
                8,
                Math.round(
                    (
                        currentStep /
                        maxIndex
                    ) * 100
                )
            );


        const progressBar =
            document.getElementById(
                "progressBar"
            );


        if (progressBar) {

            progressBar.style.width =
                progress + "%";
        }


        if (
            notify &&
            currentProject
        ) {

            showToast(
                workflowNames[currentStep] +
                " workspace selected.",
                "success",
                currentProject.name
            );
        }
    }


    function openModule(
        moduleName,
        step
    ) {

        activateNav(
            moduleName
        );


        activateStep(
            step
        );


        if (!currentProject) {

            showToast(
                "Create a film project first, then continue with this workspace.",
                "error",
                "No film selected"
            );

            return;
        }


        if (
            moduleName !== "new" &&
            moduleName !== "projects"
        ) {

            showToast(
                workflowNames[step] +
                " workspace is ready for the next ACOS module integration.",
                "success",
                "ACOS Studio"
            );
        }
    }


    function quickAction(
        action
    ) {

        const steps = {

            script: 1,

            characters: 2,

            storyboard: 3,

            video: 5

        };


        const names = {

            script: "Script",

            characters: "Characters",

            storyboard: "Storyboard",

            video: "Video Generation"

        };


        if (
            typeof steps[action] !==
            "number"
        ) {

            return;
        }


        activateNav(
            action
        );


        activateStep(
            steps[action]
        );


        if (!currentProject) {

            showToast(
                "Create a film project first.",
                "error",
                names[action]
            );

            return;
        }


        showToast(
            names[action] +
            " workspace selected.",
            "success",
            currentProject.name
        );
    }


    /*
     * ========================================================
     * IMPORT SCRIPT
     * ========================================================
     */

    function importScript() {

        openModal(
            "importModal"
        );
    }


    function handleScriptFile(
        event
    ) {

        const file =
            event.target.files &&
            event.target.files[0];


        const info =
            document.getElementById(
                "importInfo"
            );


        if (!file) {

            importedScriptText = "";

            return;
        }


        const reader =
            new FileReader();


        reader.onload =
            function () {

                importedScriptText =
                    String(
                        reader.result ||
                        ""
                    );


                const size =
                    Math.round(
                        file.size / 1024
                    );


                info.textContent =
                    file.name +
                    " selected • " +
                    size +
                    " KB • " +
                    importedScriptText.length +
                    " characters";
            };


        reader.onerror =
            function () {

                importedScriptText = "";

                info.textContent =
                    "Could not read this file.";
            };


        reader.readAsText(
            file
        );
    }


    function processImportedScript() {

        `Import script logic here`
    }


    /*
     * ========================================================
     * PREVIEW
     * ========================================================
     */

    function previewFilm() {

        if (!currentProject) {

            showToast(
                "Create a film project before previewing it.",
                "error",
                "Film Preview"
            );

            return;
        }


        showToast(
            "Preview becomes available after media generation.",
            "success",
            "Film Preview"
        );
    }


    /*
     * ========================================================
     * DOCUMENTATION / HEALTH
     * ========================================================
     */

    function openDocs() {

        window.open(
            "/docs",
            "_blank"
        );
    }


    function openHealth() {

        window.open(
            "/api/health",
            "_blank"
        );
    }


    /*
     * ========================================================
     * KEYBOARD
     * ========================================================
     */

    document.addEventListener(
        "keydown",
        function (event`sys_args`) {

            if (
                event.key === "Escape"
            ) {

                document
                    .querySelectorAll(
                        ".modal-backdrop.open"
                    )
                    .forEach(
                        modal =>
                            modal.classList.remove(
                                "open"
                            )
                    );


                document.body.style.overflow =
                    "";
            }

        }
    );


    /*
     * ========================================================
     * INITIALIZE
     * ========================================================
     */

    document.addEventListener(
        "DOMContentLoaded",
        async function () {

            activateStep(
                0,
                false
            );

            // Initialize multi-language system
            await initLanguageSystem();

            await loadProjects(
                true
            );

        }
    );

</script>


</body>

</html>
"""
