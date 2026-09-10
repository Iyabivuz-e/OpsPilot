from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from core.settings import settings
from models.models import Base
from pgvector.asyncpg import register_vector
from sqlalchemy import event,text


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

@event.listens_for(engine.sync_engine, "connect") 
def register_pgvector(dbapi_connection, connection_record): 
    """ Register pgvector on every underlying asyncpg connection. 
    SQLAlchemy gives us an AdaptedConnection here, whose run_async() 
    method lets us execute asyncpg-specific code. """ 
    dbapi_connection.run_async(register_vector)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    # class=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
        ## We dont need to close the session because async with will do it by default


# For development. Later we shall use alembic for production
async def create_tables():
    async with engine.begin() as conn:  # We establish the connection
        # We create the vector extension to work with the vectordb(pgvector)
        # await conn.execute(text('CREATE EXTENSION IF NOT EXISTS vector'))
        # We register the vectordb(pgvector) with the engine, so that we can use it in our models
        # await register_vector(conn)
        await conn.run_sync(Base.metadata.create_all)

