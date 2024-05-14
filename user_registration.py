from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create a SQLAlchemy engine to connect to a SQLite database
# Change the database URL as per your requirements
DATABASE_URL = "sqlite:///user_database.db"
engine = create_engine(DATABASE_URL, echo=True)  # Set echo=True for debugging

# Create a session factory
Session = sessionmaker(bind=engine)

# Declare a base class for our ORM models
Base = declarative_base()


# Define the User model
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)

    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"


def create_database():
    """Create the database schema based on defined models."""
    Base.metadata.create_all(engine)


def register_user(username, email, password):
    """Register a new user and add to the database."""
    session = Session()

    # Check if the username or email already exists
    if session.query(User).filter_by(username=username).first() is not None:
        session.close()
        raise ValueError("Username already exists. Please choose a different username.")

    if session.query(User).filter_by(email=email).first() is not None:
        session.close()
        raise ValueError("Email already registered. Please use a different email address.")

    # Create a new User instance
    new_user = User(username=username, email=email, password=password)

    # Add the user to the session and commit to the database
    session.add(new_user)
    session.commit()

    session.close()
    print(f"User '{username}' registered successfully!")


if __name__ == "__main__":
    # Create the database schema if not already created
    create_database()

    # Example usage: Register a new user
    try:
        register_user(username="john_doe", email="john@example.com", password="password123")
    except ValueError as e:
        print(f"Error: {e}")
