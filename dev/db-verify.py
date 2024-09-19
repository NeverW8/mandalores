from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

# Your connection string
# example: postgresql://user:password@localhost:5432/dbname
engine = create_engine("")

try:
    # Try to establish a connection
    with engine.connect() as connection:
        # Optionally, execute a simple query to verify
        result = connection.execute(text("SELECT 1"))
        if result.fetchone():
            print("Connection accepted")
except OperationalError:
    # Catch connection errors and print a clean message
    print("Couldn't establish a connection. Please ensure the database is running and accessible.")
