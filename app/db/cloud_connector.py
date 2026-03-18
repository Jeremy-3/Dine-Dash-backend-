from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from google.cloud.sql.connector import Connector, IPTypes
from app.core.config import settings
from app.db.base import Base


def init_connection_engine(connector: Connector) -> Engine:
    ip_type = IPTypes.PRIVATE if settings.PRIVATE_IP else IPTypes.PUBLIC

    user, enable_iam_auth = (
        (settings.DB_IAM_USER, True)
        if settings.DB_IAM_USER
        else (settings.DB_USER, False)
    )

    def getconn():
        return connector.connect(
            settings.DB_INSTANCE,
            "pg8000",
            user=user,
            password=settings.DB_PASS,
            db=settings.DB_NAME,
            ip_type=ip_type,
            enable_iam_auth=enable_iam_auth,
        )

    engine = create_engine(
        "postgresql+pg8000://",
        creator=getconn,
        pool_pre_ping=True,
    )

    return engine


connector = Connector()
engine = init_connection_engine(connector)

DB_Session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)
