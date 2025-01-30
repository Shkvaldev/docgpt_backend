from mongodb.models import Doc
from mongodb.services import MongoBaseService

class DocService:
    """
    Service for using `Doc` model in mongodb
    """
    def __init__(self) -> None:
        self.model = Doc
