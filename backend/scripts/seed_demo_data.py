from app.core.database import Base, engine
from app.mock_data.demo_data import seed_demo_data
from app import models  # noqa: F401


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    seed_demo_data()
    print("Demo data seeded successfully.")

