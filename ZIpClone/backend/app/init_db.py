"""
Database initialization script
Run this to create initial admin and manager users
"""
from app.database import SessionLocal, engine, Base
from app.models import User, UserRole
from app.auth import get_password_hash

def init_db():
    """Initialize database with default users"""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    try:
        # Check if admin exists
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            admin = User(
                username="admin",
                email="admin@procurement.com",
                hashed_password=get_password_hash("admin123"),
                full_name="Admin User",
                role=UserRole.ADMIN
            )
            db.add(admin)
            print("Created admin user: admin / admin123")
        
        # Check if manager exists
        manager = db.query(User).filter(User.username == "manager").first()
        if not manager:
            manager = User(
                username="manager",
                email="manager@procurement.com",
                hashed_password=get_password_hash("manager123"),
                full_name="Manager User",
                role=UserRole.MANAGER
            )
            db.add(manager)
            print("Created manager user: manager / manager123")
        
        # Check if test user exists
        test_user = db.query(User).filter(User.username == "user").first()
        if not test_user:
            test_user = User(
                username="user",
                email="user@procurement.com",
                hashed_password=get_password_hash("user123"),
                full_name="Test User",
                role=UserRole.USER
            )
            db.add(test_user)
            print("Created test user: user / user123")
        
        db.commit()
        print("Database initialized successfully!")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()

