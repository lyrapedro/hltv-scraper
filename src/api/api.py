from fastapi import APIRouter, Query, Request
from slowapi import Limiter
from slowapi.util import get_remote_address

from src.core.scrapers.main import check_health
from src.core.cs import Cs
from src.core.vlr import Vlr

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)
cs = Cs()
vlr = Vlr()

"""CS endpoints"""

@router.get("/cs/events")
@limiter.limit("100/minute")
async def CS_events(request: Request, event_type: int = 0):
    """
    query parameters:\n
        "event_type": type of event\n
            ALL = 0
            MAJOR = 1
            INTERNATIONAL_LAN = 2
            REGIONAL_LAN = 3
            ONLINE = 4
            LOCAL_LAN = 5
    """
    return await cs.cs_current_events(event_type)

@router.get("/cs/event/matches")
@limiter.limit("100/minute")
async def CS_event_live_matches(request: Request, event_id: str):
    """
        query parameters:\n
            "event_id": ID of event\n
    """
    return await cs.cs_live_matches(event_id)

@router.get("/cs/matches")
@limiter.limit("100/minute")
async def CS_matches(request: Request):
    return await cs.cs_all_live_matches()


"""VLR endpoints"""

@router.get("/vlr/events")
@limiter.limit("100/minute")
async def VLR_events(request: Request):
    return await vlr.vlr_current_events()

@router.get("/vlr/event/matches")
@limiter.limit("100/minute")
async def VLR_event_live_matches(request: Request, event_url: str):
    return await vlr.vlr_live_matches(event_url)

@router.get("/vlr/matches")
@limiter.limit("100/minute")
async def VLR_matches(request: Request):
    return await vlr.vlr_all_live_matches()


@router.get("/health")
def health():
    return check_health()