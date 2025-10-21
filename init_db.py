# init_db.py
from website import create_app, db

# Create the app instance
app = create_app()

# Push an application context (required by Flask-SQLAlchemy)
with app.app_context():
    db.create_all()
    print("Database created successfully at: instance/sitedata.sqlite")
