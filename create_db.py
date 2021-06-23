from app.models.database import db, base

base.metadata.create_all(db)
