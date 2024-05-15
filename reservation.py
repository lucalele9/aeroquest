from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# Create a SQLAlchemy engine to connect to a SQLite database
# Change the database URL as per your requirements
DATABASE_URL = "sqlite:///reservation_database.db"
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

    reservations = relationship("Reservation", back_populates="user")


# Define the Reservation model
class Reservation(Base):
    __tablename__ = 'reservations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship("User", back_populates="reservations")
    flight_number = Column(String(20), nullable=False)
    departure_date = Column(DateTime, nullable=False)
    seat_number = Column(String(10), nullable=True)

    def __repr__(self):
        return f"<Reservation(user_id={self.user_id}, flight_number='{self.flight_number}', departure_date='{self.departure_date}', seat_number='{self.seat_number}')>"


def create_database():
    """Create the database schema based on defined models."""
    Base.metadata.create_all(engine)


def create_reservation(user_id, flight_number, departure_date, seat_number=None):
    """Create a new reservation and add to the database."""
    session = Session()

    # Check if user_id exists
    user = session.query(User).filter_by(id=user_id).first()
    if not user:
        session.close()
        raise ValueError(f"User with id {user_id} does not exist.")

    # Create a new Reservation instance
    new_reservation = Reservation(
        user_id=user_id,
        flight_number=flight_number,
        departure_date=datetime.strptime(departure_date, "%Y-%m-%d %H:%M:%S"),
        seat_number=seat_number
    )

    # Add the reservation to the session and commit to the database
    session.add(new_reservation)
    session.commit()

    session.close()
    print(f"Reservation created successfully for user '{user.username}'!")


if __name__ == "__main__":
    # Create the database schema if not already created
    create_database()

    # Example usage: Create a reservation for a user
    try:
        create_reservation(user_id=1, flight_number="ABC123", departure_date="2024-05-15 10:00:00", seat_number="A1")
    except ValueError as e:
        print(f"Error: {e}")
