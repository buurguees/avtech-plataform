"""
AVTech Platform - Database Migration Script
===========================================

Script for running database migrations using Alembic.
"""

import asyncio
import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.backend.database.connection import engine
from src.backend.database.models import Base


async def create_tables():
    """Create all database tables."""
    print("🔄 Creating database tables...")
    
    async with engine.begin() as conn:
        # Import all models to ensure they are registered
        from src.backend.database import models
        
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
    
    print("✅ Database tables created successfully!")


async def drop_tables():
    """Drop all database tables."""
    print("🗑️  Dropping database tables...")
    
    async with engine.begin() as conn:
        # Import all models to ensure they are registered
        from src.backend.database import models
        
        # Drop all tables
        await conn.run_sync(Base.metadata.drop_all)
    
    print("✅ Database tables dropped successfully!")


async def reset_database():
    """Reset the database by dropping and recreating all tables."""
    print("🔄 Resetting database...")
    await drop_tables()
    await create_tables()
    print("✅ Database reset successfully!")


def main():
    """Main function for running migrations."""
    import argparse
    
    parser = argparse.ArgumentParser(description="AVTech Platform Database Migration")
    parser.add_argument(
        "action",
        choices=["create", "drop", "reset"],
        help="Action to perform: create, drop, or reset tables"
    )
    
    args = parser.parse_args()
    
    if args.action == "create":
        asyncio.run(create_tables())
    elif args.action == "drop":
        asyncio.run(drop_tables())
    elif args.action == "reset":
        asyncio.run(reset_database())


if __name__ == "__main__":
    main()
