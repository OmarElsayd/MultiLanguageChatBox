from sqlalchemy.orm import sessionmaker
from rtvt_services.db_engine.engine import create_db_engine

engine = create_db_engine()
LocalSession = sessionmaker(bind=engine)

print(LocalSession)
