from http.client import HTTPException
from app.api.dependencies import get_cache
from app.models.wireframe import WireframeRequest, WireframeResponse
from app.services.wireframe.graph import generate_wireframe
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from fastapi.responses import JSONResponse
import time
from typing import List, Dict, Any, Optional



router = APIRouter()

@router.post("/generate", response_model=WireframeResponse)
async def create_wireframe(
    request: WireframeRequest, 
    background_tasks: BackgroundTasks, 
    cache= Depends(get_cache)
    ):
    """
    Generate a wireframe from a user query.
    
    Args:
        request: The user's description of the desired wireframe
        
    Returns:
        State containing the generated wireframe and intermediary data
    """

    if cache:
        cache_result = cache.get(request.user_query)
        if cache_result:
            return cache_result

    try:
        # generate the wireframe
        result = generate_wireframe(request.user_query)

        # check for errors
        if result.get("errors") and len(result['errors']) > 0:
            raise HTTPException(
                status_code=500, 
                detail={
                    "message": "Error generating wireframe",
                    "detailed_requirements": result['detailed_requirements'],
                    "wireframe_plan": result['wireframe_plan'],
                    "svg_code": result['svg_code'],
                    "errors": result['errors']
                }
            )
        
        # Prepare the response
        respnonse = WireframeResponse(
            svg_code = result['svg_code'],
            detailed_requirements = result.get('detailed_requirements'), 
            wireframe_plan = result.get('wireframe_plan'),
            errors = result.get('errors'),
            status = 200
        )

        # store in cache if enabled
        if cache:
            background_tasks.add_task(cache.set, request.user_query, respnonse)

        return respnonse
    
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "message": f"Error generating wireframe: {str(e)}"
            }
        )
    

@router.get("/health")
async def health_check():
    """
    Check the health of the API.
    """
    return {"status": "healthy", "timestamp": time.time()}


