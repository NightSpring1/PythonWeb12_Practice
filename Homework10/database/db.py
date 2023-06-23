from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.models import Base

postgres = ''


engine = create_engine(postgres)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

if __name__ == '__main__':
    session = Session()
