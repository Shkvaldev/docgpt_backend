from db.models.users import User
from db.models.chats import Chat
from db.models.messages import Message
from db.models.files import File
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.base_model import Model as Base

# Создаем движок SQLite
engine = create_engine("sqlite:///test.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Создаем тестовые данные
# 1. Создаем пользователя
user = User(
    name="John Doe",
    email="john@example.com",
    password_hash="hashed_password"
)
session.add(user)
session.commit()

# 2. Создаем чат для пользователя
chat = Chat(user=user)
session.add(chat)
session.commit()

# 3. Создаем файл
file = File(path="/path/to/file.txt")
session.add(file)
session.commit()

# 4. Создаем сообщения (одно с файлом, одно без)
message1 = Message(
    content="Hello with file!",
    chat=chat,
    file=file
)
message2 = Message(
    content="Hello without file!",
    chat=chat
)
session.add_all([message1, message2])
session.commit()

# Проверяем связи
print("\nПроверка пользователя:")
print(f"Имя пользователя: {user.name}")
print(f"Количество чатов: {len(user.chats)}")

print("\nПроверка чата:")
print(f"ID чата: {chat.id}")
print(f"Владелец чата: {chat.user.name}")
print(f"Количество сообщений: {len(chat.messages)}")

print("\nПроверка сообщений:")
for msg in chat.messages:
    print(f"Сообщение: {msg.content}")
    print(f"Прикрепленный файл: {'Есть' if msg.file_id else 'Нет'}")

print("\nПроверка файла:")
print(f"Путь к файлу: {file.path}")
print(f"Связанное сообщение ID: {file.message[0].id if file.message else 'Нет'}")

# Проверяем каскадное удаление
session.delete(user)
session.commit()

# Проверяем, что все связанные объекты удалены
print("\nПроверка каскадного удаления:")
print(f"Осталось чатов: {len(session.query(Chat).all())}")
print(f"Осталось сообщений: {len(session.query(Message).all())}")
print(f"Осталось файлов: {len(session.query(File).all())}")

session.close()
