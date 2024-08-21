import uvicorn
from sqlalchemy.orm import Session
from fastapi import FastAPI, Request, Depends, HTTPException, status

from src.database.db import get_db
from src.database.models import User, Role
from src.routes import routes_auth
from src.routes import admin as routes_admin
from src.routes import user as routes_user

from src.routes import venicle as vehicle_router
from src.routes import report
from src.routes import message as message


app = FastAPI()

app.include_router(routes_auth.router, prefix="/api")
app.include_router(routes_admin.router, prefix="/api")
app.include_router(routes_user.router, prefix="/api")
app.include_router(vehicle_router.router, prefix="/api")
app.include_router(report.router, prefix="/reports")
app.include_router(message.router, prefix='/api')

@app.get("/", status_code=status.HTTP_200_OK)
async def static(request: Request, db: Session = Depends(get_db)):
    # create role
    roles = ["Admin", "Moderator", "User"]
    for role_name in roles:
        existing_role = db.query(Role).filter(Role.role == role_name).first()
        if not existing_role:
            db.add(Role(role=role_name))
    db.commit()
    return "OK"


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) # , reload=True