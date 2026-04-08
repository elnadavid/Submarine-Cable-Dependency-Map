from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import cables

# ─────────────────────────────────────────────
#  THE APP
#  This is the entry point. Think of it as the
#  "front door" of your backend server.
# ─────────────────────────────────────────────
app = FastAPI(
    title="Submarine Cable Dependency Map API",
    description="Real Rails PoC #24 — Backend data service for submarine cable intelligence.",
    version="1.0.0"
)

# ─────────────────────────────────────────────
#  CORS MIDDLEWARE
#  This is critical for full-stack development.
#  Without this, your Next.js frontend (running
#  on port 3000) would be BLOCKED from calling
#  this backend (running on port 8000).
#  CORS = Cross-Origin Resource Sharing.
# ─────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Only allow our frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────────────────────────────────────
#  REGISTER ROUTES
#  We attach our cables router under /api
#  So all cable endpoints become /api/cables,
#  /api/landing-stations, etc.
# ─────────────────────────────────────────────
app.include_router(cables.router, prefix="/api")


# ─────────────────────────────────────────────
#  ROOT HEALTH CHECK
#  A simple endpoint to confirm the server is up
# ─────────────────────────────────────────────
@app.get("/")
def root():
    return {
        "status": "online",
        "project": "Submarine Cable Dependency Map",
        "poc": 24,
        "message": "Real Rails backend is running. Visit /docs for API explorer."
    }
