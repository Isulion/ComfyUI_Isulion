"""
HTTP routes for the Mega Prompt V4 preview (web/mega_prompt_v4.js).

The handlers are thin wrappers around pure functions so they can be tested
without ComfyUI's PromptServer or aiohttp, which only exist inside ComfyUI.
"""

import asyncio
import logging

from .mega_prompt_v4 import REEL_NAMES, list_themes, new_seed, parse_state, roll

try:
    from aiohttp import web
except ImportError:  # test environment
    web = None

logger = logging.getLogger(__name__)

ROUTE_PREFIX = "/isulion/megaprompt_v4"


def themes_payload():
    return list_themes()


def roll_payload(body):
    """Validate a POST /roll body and roll; returns (status, payload)."""
    if not isinstance(body, dict):
        return 400, {"error": "body must be a JSON object"}
    reels = body.get("reels", list(REEL_NAMES))
    if not isinstance(reels, list) or any(r not in REEL_NAMES for r in reels):
        return 400, {"error": "unknown reel"}
    seed = body.get("seed")
    if isinstance(seed, bool) or not isinstance(seed, int) or not 0 <= seed < 2**32:
        seed = new_seed()
    return 200, roll(parse_state(body.get("state")), reels, seed)


def _json(payload, status):
    if web is None:
        return status, payload
    return web.json_response(payload, status=status)


def register_routes(server_instance=None):
    inst = server_instance
    if inst is None:
        try:
            from server import PromptServer
            inst = PromptServer.instance
        except Exception:
            inst = None
    if inst is None:
        return False

    @inst.routes.get(f"{ROUTE_PREFIX}/themes")
    async def themes(request):
        return _json(themes_payload(), 200)

    @inst.routes.post(f"{ROUTE_PREFIX}/roll")
    async def roll_route(request):
        try:
            body = await request.json()
        except Exception:
            body = None
        # theme handlers are synchronous: keep them off the aiohttp loop
        status, payload = await asyncio.to_thread(roll_payload, body)
        return _json(payload, status)

    return True


ROUTES_REGISTERED = register_routes()
