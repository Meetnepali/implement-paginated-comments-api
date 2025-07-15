from fastapi import FastAPI, HTTPException, status, Depends, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, constr, validator
from typing import Dict, Optional

app = FastAPI()

# In-memory data store
data_store: Dict[str, dict] = {}

def get_store():
    return data_store

class UserPreferences(BaseModel):
    language: constr(min_length=2, max_length=10)
    notifications_enabled: bool
    theme: constr(min_length=3, max_length=32)

    @validator("language")
    def validate_language(cls, v):
        allowed_languages = {"en", "es", "fr", "de", "it", "zh"}
        if v not in allowed_languages:
            raise ValueError(f"Unsupported language: {v}")
        return v

    @validator("theme")
    def validate_theme(cls, v):
        allowed_themes = {"light", "dark"}
        if v not in allowed_themes:
            raise ValueError(f"Unsupported theme: {v}")
        return v

class UserPreferencesResponse(UserPreferences):
    user_id: str

class ErrorResponse(BaseModel):
    detail: str

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@app.post("/preferences/{user_id}", response_model=UserPreferencesResponse, responses={
    409: {"model": ErrorResponse},
    422: {"model": ErrorResponse}
}, status_code=201)
def create_preferences(user_id: str, preferences: UserPreferences, store: dict = Depends(get_store)):
    if user_id in store:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Preferences for user '{user_id}' already exist."
        )
    store[user_id] = preferences.dict()
    return {**preferences.dict(), "user_id": user_id}

@app.get("/preferences/{user_id}", response_model=UserPreferencesResponse, responses={
    404: {"model": ErrorResponse}
})
def get_preferences(user_id: str, store: dict = Depends(get_store)):
    prefs = store.get(user_id)
    if not prefs:
        raise HTTPException(status_code=404, detail=f"Preferences for user '{user_id}' not found.")
    return {**prefs, "user_id": user_id}

@app.put("/preferences/{user_id}", response_model=UserPreferencesResponse, responses={
    404: {"model": ErrorResponse},
    422: {"model": ErrorResponse}
})
def update_preferences(user_id: str, preferences: UserPreferences, store: dict = Depends(get_store)):
    if user_id not in store:
        raise HTTPException(status_code=404, detail=f"Preferences for user '{user_id}' not found.")
    store[user_id] = preferences.dict()
    return {**preferences.dict(), "user_id": user_id}

@app.delete("/preferences/{user_id}", status_code=204, responses={
    404: {"model": ErrorResponse}
})
def delete_preferences(user_id: str, store: dict = Depends(get_store)):
    if user_id not in store:
        raise HTTPException(status_code=404, detail=f"Preferences for user '{user_id}' not found.")
    del store[user_id]
    return