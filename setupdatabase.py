from main import db,app
app.app_context().push()
db.create_all()