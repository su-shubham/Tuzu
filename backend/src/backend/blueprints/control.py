from quart import Blueprint, ResponseReturnValue

blueprint = Blueprint("control", __name__)


@blueprint.get("/control")
async def control() -> ResponseReturnValue:
    return {"ping": "control"}
