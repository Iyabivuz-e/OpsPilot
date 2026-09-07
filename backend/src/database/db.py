from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from core.settings import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,  # This should be False in production ofcourse
    future=True,
    pool_size=20, 
    max_overflow=0, 
    pool_pre_ping=True,
    pool_recycle=3600, 
)

AsyncSessionLocal = AsyncSession(
    engine,
    # class=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False 
)

async def get_db() -> AsyncSession:
    with AsyncSessionLocal() as session:
        try:
             yield session
        finally:
            await session.close()
        