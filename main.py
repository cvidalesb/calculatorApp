from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, users, data, admin
import uvicorn

# Create FastAPI instance
app = FastAPI(
    title="FastAPI Backend with Role-Based Access",
    description="A FastAPI backend application with role-based access control",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(data.router)
app.include_router(admin.router)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "FastAPI Backend with Role-Based Access is running", 
        "version": "1.0.0",
        "endpoints": {
            "auth": "/auth",
            "users": "/users",
            "data": "/data",
            "admin": "/admin",
            "docs": "/docs"
        }
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is running"}

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
