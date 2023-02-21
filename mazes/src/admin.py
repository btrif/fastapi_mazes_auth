#  Created by btrif Trif on 21-02-2023 , 6:02 PM.


from fastapi import APIRouter

router_admin = APIRouter()


@router_admin.post("/admin")
async def update_admin():
    return {"message": "Admin getting schwifty"}
