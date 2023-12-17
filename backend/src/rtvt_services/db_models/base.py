from sqlalchemy.orm import declarative_base
from sqlalchemy import MetaData


metadata = MetaData(schema="rtvt_database")
Base = declarative_base(metadata=metadata)
