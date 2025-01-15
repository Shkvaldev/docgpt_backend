from fastapi import HTTPException, UploadFile
from fastapi.responses import FileResponse
import os
import mimetypes
import aiofiles # Добавить в рек!!!


from api.services.base import BaseService
from db.models import File_doc
from config import settings

class FilesService:
    """
    Сервис для работы с файлами
    """
    def __init__(self):
        self.model = File_doc

    @staticmethod
    async def generate_message_dict(file: File_doc) -> dict:
        """
        Генерация информации о файле в виде словаря 
        """
        if not file:
            return {}
        return {
            'id': file.id,
            'path': file.path,
            'created': file.created_at.strftime(format=settings.date_time_format)
        }
    
    async def check_file_access(self, id: int, user_id: int) -> File_doc:
        """
        Проверка доступа пользователя к файлу
        """
        file = await BaseService().get(self.model, id=id)
        if not file:
            raise HTTPException(
                status_code=404,
                detail='File was not found in database'
            )
            
        if file.user_id != user_id:
            raise HTTPException(
                status_code=401,
                detail='Cannot access to this user with your session',
            )
            
        return file
    
    async def create(self, path: str, file: UploadFile, user_id: int) -> dict:
        """
        Создание нового файла
        """
        # Сохраняем файл
        file_path = f"{settings.upload_dir}/{path}"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        # Создаем запись в БД
        file_db = await BaseService().create(
            self.model,
            path=f"static/{path}",
            user_id=user_id
        )
        
        return {
            'status': 'ok',
            'file_id': file_db.id
        }

    async def get_file(self, id: int, user_id: int) -> FileResponse:
        """
        Получение файла по id
        """
        file_db = await self.check_file_access(id, user_id)
        content_type, _ = mimetypes.guess_type(file_db.path)
        
        if not os.path.exists(file_db.path):
            print(file_db.path)
            raise HTTPException(status_code=404, detail='File does not exist on the server')
        
        return FileResponse(
            path=file_db.path,
            filename=os.path.basename(file_db.path),
            media_type=content_type or 'application/octet-stream'
        )
    
    async def get_files(self, user_id: int) -> dict:
        """
        Получение всех файлов пользователя
        """
        files_db = await BaseService().get_all(self.model, user_id=user_id)
        if not files_db:
            raise HTTPException(
                status_code=404,
                detail='File was not found'
            )
        return {
            'status': 'ok',
            'files': [await FilesService.generate_message_dict(file) for file in files_db]
        }

    async def delete(self, id: int, user_id: int) -> dict:
        """
        Удаление файла
        """
        file_db = await self.check_file_access(id, user_id)
        
        if os.path.exists(file_db.path):
            try:
                os.remove(file_db.path)
            except OSError as e:
                raise HTTPException(
                    status_code=500,
                    detail=f'Failed to delete file from disk: {str(e)}'
                )
        
        await BaseService().delete(self.model, id=id)
        
        return {
            'status': 'ok'
        }