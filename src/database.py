from sqlmodel import SQLModel, Session, create_engine

engine = create_engine("sqlite:///./hackerschool.db", echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
