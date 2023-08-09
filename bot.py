import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.orm import declarative_base, sessionmaker

# Настройки для подключения к базе данных
DATABASE_URL = 'postgresql://django:django@localhost/admin_bot'
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

# Описание модели таблицы keywords_users
class User(Base):
    __tablename__ = 'keywords_users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    user_id = Column(Integer, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String)

# Описание модели таблицы keywords_keywords
class Keyword(Base):
    __tablename__ = 'keywords_keywords'
    keyword = Column(String, primary_key=True)
    photo_url = Column(String)
    text = Column(String)

# Инициализация логгера
logging.basicConfig(level=logging.DEBUG)

# Инициализация бота и диспетчера
bot = Bot(token='YOUR_BOT_TOKEN')
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Обработка команды /start
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    user = message.from_user
    user_id = user.id
    first_name = user.first_name
    last_name = user.last_name
    username = user.username

    session = Session()
    existing_user = session.query(User).filter_by(user_id=user_id).first()

    if not existing_user:
        new_user = User(user_id=user_id, first_name=first_name, last_name=last_name, username=username)
        session.add(new_user)
        session.commit()

    session.close()

    await message.reply(f"Привет, {first_name}! Д
