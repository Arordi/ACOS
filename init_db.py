from core.database import Base, engine
from models import Project, MediaFile


def init_database():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_database()
    print("ACOS database initialized successfully.")
