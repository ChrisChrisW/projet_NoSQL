from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

# Configuration PostgresDB
class PostgresDB:
    # PostgreSQL configuration
    postgres_uri = os.getenv('POSTGRES_DB_URI')
    if not postgres_uri:
        raise ValueError("POSTGRES_DB_URI environment variable is not set.")
    engine = create_engine(postgres_uri)
    Base = declarative_base()

    class PostgresItem(Base):
        __tablename__ = 'postgres_items'
        id = Column(Integer, primary_key=True)
        field1 = Column(String(255), nullable=False)
        field2 = Column(String(255), nullable=False)

    def __init__(self):
        self.setup_database()

    def setup_database(self):
        self.Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def get_items(self):
        try:
            return self.session.query(self.PostgresItem).all()
        except Exception as e:
            print(f"Error during database operation: {e}")
            return []
    
    def get_item_by_id(self, item_id):
        return self.session.query(self.PostgresItem).filter_by(id=item_id).first()

    def create_items(self, data):
        try:
            for item in data:
                postgres_item = self.PostgresItem(**item)
                self.session.add(postgres_item)
            self.session.commit()
        except Exception as e:
            print(f"Error during database operation: {e}")
            self.session.rollback()


    def create_item(self, field1, field2):
        data = {
            'field1': field1,
            'field2': field2
        }
        postgres_item = self.PostgresItem(**data)
        self.session.add(postgres_item)
        self.session.commit()

    def edit_item(self, item_id, new_field1, new_field2):
        item = self.get_item_by_id(item_id)
        item.field1 = new_field1
        item.field2 = new_field2
        self.session.commit()

    def delete_items(self):
        self.session.query(self.PostgresItem).delete()
        self.session.commit()

    def delete_item(self, item_id):
        item = self.get_item_by_id(item_id)
        self.session.delete(item)
        self.session.commit()