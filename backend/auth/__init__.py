
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from .user_manager import delete_account, generate_api_key

router = APIRouter()

@router.post("/auth/generate_api_key")
async def generate_api_key_endpoint(request: Request):
	body = await request.json()
	user_id = body.get("user_id")
	result = generate_api_key(user_id)
	if result.get("success") is True:
		return JSONResponse(
			content={"success": True, "api_key": result.get("api_key")},
			status_code=200
		)
	if result.get("success") is not True:
		raise HTTPException(
			status_code=400,
			detail=result.get("error", "API key generation failed")
		)

@router.post("/auth/delete_account")
async def delete_account_endpoint(request: Request):
	body = await request.json()
	user_id = body.get("user_id")
	result = delete_account(user_id)
	if result.get("success"):
		return result
	else:
		return JSONResponse(
			content={"error": result.get("error", "Account deletion failed")},
			status_code=400
		)

from .access_manager import check_access

__all__ = ["router"]
