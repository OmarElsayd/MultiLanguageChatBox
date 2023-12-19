from sqlalchemy.orm import declarative_base
from sqlalchemy import MetaData

from rtvt_services.util.constant import DB_SCHEMA

metadata = MetaData(schema=DB_SCHEMA)
Base = declarative_base(metadata=metadata)
