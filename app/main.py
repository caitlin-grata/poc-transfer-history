import os
import time
from sqlalchemy import (
    create_engine,text, Column, Integer, String, Enum, ForeignKey,
)
from sqlalchemy.orm import declarative_base, sessionmaker,  relationship
from sqlalchemy.exc import OperationalError
import enum

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://myuser:mypassword@db:5432/mydb")

def get_db_connection(max_retries=5, retry_interval=5):
    for i in range(max_retries):
        try:
            engine = create_engine(DATABASE_URL)
            # Test the connection
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return engine
        except OperationalError as e:
            if i < max_retries - 1:
                print(f"Database connection attempt {i + 1} failed. Retrying in {retry_interval} seconds...")
                time.sleep(retry_interval)
            else:
                raise e

engine = get_db_connection()
Session = sessionmaker(bind=engine)
Base = declarative_base()


def init_db():
    Base.metadata.create_all(engine)
    print("Database tables created successfully")


#  DB models
class StatusEnum(str, enum.Enum):
    active = 'active'
    inactive = 'inactive'

class TypeEnum(str, enum.Enum):
    primary = 'primary'
    secondary = 'secondary'
    foreign_language = 'foreign_language'


class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    # One-to-many relationship with Domain
    domains = relationship("Domain", back_populates="company", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Company(id={self.id}, name='{self.name}')>"


class Domain(Base):
    __tablename__ = 'domains'

    id = Column(Integer, primary_key=True)
    domain = Column(String, nullable=False)
    status = Column(Enum(StatusEnum, name="status_enum"), nullable=False)
    type = Column(Enum(TypeEnum, name="type_enum"), nullable=False)
    company_id = Column(Integer, ForeignKey('companies.id', ondelete="CASCADE"), nullable=False)

    company = relationship("Company", back_populates="domains")

    def __repr__(self):
        return (
            f"<Domain(id={self.id}, domain='{self.domain}', status='{self.status}', "
            f"type='{self.type}', company_id={self.company_id})>"
        )

# Methods

def list_companies():
    with Session() as session:
        companies = session.query(Company).all()
        for company in companies:
            print(f"\nCompany {company.id}: {company.name}")
            print("Domains:")
            for domain in company.domains:
                print(f"  - {domain.domain} ({domain.status}, {domain.type})")

def parent_company_redirect(company, sub_company):
    # make sub_company inactive
    # move all domains to company as inactive, and redirect
    pass



if __name__ == "__main__":
    # Initialize database tables
    init_db()
    try:
        while True:
            continue
    except KeyboardInterrupt:
        print("\nApplication shutdown requested. Exiting...")