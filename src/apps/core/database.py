from sqlalchemy import create_engine, NullPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from core.config import settings

engine_async = create_async_engine(settings.db.async_database_url,
                                   poolclass=NullPool,
                                   future=True,
                                   echo=True, )
async_session_maker = async_sessionmaker(engine_async,
                                         expire_on_commit=False,
                                         class_=AsyncSession)

engine_sync = create_engine(settings.db.sync_database_url,
                            poolclass=NullPool,
                            future=True,
                            echo=True, )
sync_session_maker = sessionmaker(engine_sync,
                                  expire_on_commit=False,
                                  class_=Session)
