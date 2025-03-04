from quart import Blueprint, request, render_template
from loguru import logger

from admin.utils import auth_required
from mongodb.services import MongoBaseService
from mongodb.models import Doc
from mongodb.database import mongo_init

router = Blueprint(
    name='documents_router_get',
    import_name='documents_router_get'
)

@router.get('/get')
@auth_required
async def default_route():
    try:
        await mongo_init()

        # Parsing arguments
        offset = request.args.get('offset') or 0
        amount = request.args.get('amount') or 15

        documents = await MongoBaseService.find_all(
            model=Doc,
            offset=offset,
            amount=amount
        )
    except Exception as e:
        logger.error(f"Failed to get documents: {e}")
        documents = []
    return await render_template('documents/get.html', 
         documents=documents
    )
