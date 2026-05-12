from fastapi import FastAPI

app = FastAPI(title="SARA Cloud Backend", version="1.0.0")


@app.get("/")
def root():
    return {"status": "online", "service": "SARA Cloud Backend"}


@app.get("/sync")
def sync_status():
    return {
        "mobile_sync": "framework_ready",
        "cloud_profiles": "planned",
        "plugin_marketplace": "planned",
        "subscription_layer": "future_release",
    }
