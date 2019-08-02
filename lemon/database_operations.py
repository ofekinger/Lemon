from sqlalchemy import create_engine, String, Column, ARRAY, Table, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

CONNECTION_STRING = "postgres://stoprqremwbbum:6fa6ff45a4e62b6d3f85ff92483e77c0d10cee4eef13a2a11bf72cab1c031d08@ec2-" \
                    "54-217-219-235.eu-west-1.compute.amazonaws.com:5432/d8s5glfj5c13u6"

METADATA = MetaData()
TABLES = {
    "Plugins": Table(
        "Plugins",
        METADATA,
        Column("name", String, primary_key=True),
        Column("keywords", ARRAY(String))
    )
}

Base = declarative_base()


class Plugin(Base):
    __tablename__ = "Plugins"
    name = Column(String, primary_key=True)
    keywords = Column(ARRAY(String))


class DatabaseCommunication:
    def __init__(self):
        self.__engine = create_engine(CONNECTION_STRING)
        self.__init_tables()
        self.Session = sessionmaker(bind=self.__engine)

    def __init_tables(self):
        METADATA.create_all(self.__engine)

    def add_plugin(self, plugin_name, keywords):
        session = self.Session()
        session.add(Plugin(name=plugin_name, keywords=keywords))
        session.commit()

    def get_plugins(self):
        return self.Session().query(Plugin).all()

    def get_plugin(self, name):
        return self.Session().query(Plugin).filter(Plugin.name == name).one()

    def remove_plugin(self, plugin_name):
        session = self.Session()
        session.query(Plugin).filter(Plugin.name == plugin_name).delete()
        session.commit()
