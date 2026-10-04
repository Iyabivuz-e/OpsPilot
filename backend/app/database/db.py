from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from core.settings import settings
from models.models import Base
# from pgvector.asyncpg import register_vector
from sqlalchemy import event


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

## We need to register the pgvector extension with the database connection.
# @event.listens_for(engine.sync_engine, "connect") 
@event.listens_for(engine.sync_engine, "connect")
def register_vector_codec(dbapi_connection, connection_record):
    dbapi_connection.run_async(
        lambda conn: conn.set_type_codec(
            "vector",
            schema="public",          # where the pgvector extension is installed
            encoder=lambda value: value,   # SQLAlchemy already gives a '[...]' string
            decoder=lambda value: value,   # pgvector's result processor parses it back
            format="text",
        )
    )


# def register_pgvector(dbapi_connection, connection_record): 
#     dbapi_connection.run_async()

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
        await conn.run_sync(Base.metadata.create_all)

