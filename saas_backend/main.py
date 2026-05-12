from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from saas_backend.security import create_token, verify_token
from saas_backend.store import USERS, COMMAND_HISTORY, SYNC_DATA
from sara_assistant.core.command_router import CommandRouter
from sara_assistant.core.cyber_tools import CyberToolRegistry
from sara_assistant.app_info import APP_NAME, APP_VERSION

app = FastAPI(title="SARA SaaS Backend", version=APP_VERSION)
router = CommandRouter()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoginRequest(BaseModel):
    email: str
    password: str

class CommandRequest(BaseModel):
    command: str

class SyncRequest(BaseModel):
    device_id: str
    payload: dict

@app.get("/")
def root():
    return {"app": APP_NAME, "version": APP_VERSION, "status": "online"}

@app.post("/auth/login")
def login(data: LoginRequest):
    user = USERS.get(data.email)
    if not user or user["password"] != data.password:
        raise HTTPException(status_code=401, detail="Invalid login")
    return {"access_token": create_token(data.email), "user": {"email": data.email, "role": user["role"]}}

@app.get("/me")
def me(email: str = Depends(verify_token)):
    user = USERS.get(email)
    return {"email": email, "role": user["role"]}

@app.post("/command")
def command(data: CommandRequest, email: str = Depends(verify_token)):
    response = router.route(data.command)
    COMMAND_HISTORY.append({"email": email, "command": data.command, "response": response})
    return {"command": data.command, "response": response}

@app.get("/cyber/tools")
def cyber_tools(email: str = Depends(verify_token)):
    return {"tools": CyberToolRegistry.TOOLS, "notice": CyberToolRegistry.safety_notice()}

@app.post("/sync")
def sync(data: SyncRequest, email: str = Depends(verify_token)):
    SYNC_DATA.setdefault(email, {})[data.device_id] = data.payload
    return {"status": "synced", "device_id": data.device_id}

@app.get("/admin/dashboard")
def admin_dashboard(email: str = Depends(verify_token)):
    user = USERS.get(email)
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    return {
        "users": len(USERS),
        "commands": len(COMMAND_HISTORY),
        "sync_devices": sum(len(v) for v in SYNC_DATA.values()),
        "recent_commands": COMMAND_HISTORY[-10:],
    }
