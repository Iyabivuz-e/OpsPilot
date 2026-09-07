from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from core.settings import settings
from models.models import Base

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,  # This should be False in production ofcourse
    # connect_args={"ssl": "required"},
    future=True,
    pool_size=20, 
    max_overflow=0, 
    pool_pre_ping=True,
    pool_recycle=3600, 
)

AsyncSessionLocal = AsyncSession(
    bind=engine,
    # class=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False 
)

async def get_db() -> AsyncSession:
   async with AsyncSessionLocal() as session:
        yield session
        ## We dont need to close the session because async with will do it by default
        
# For development. Later we shall use alembic for production
async def create_tables():
    async with engine.begin() as conn: # We establish the connection
        await conn.run_sync(Base.metadata.create_all)