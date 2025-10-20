from website import create_app, db
from website.models import TicketType

app = create_app()
app.app_context().push()

ticket1 = TicketType(event_id=1, label='Standard', price=50, quota=100)
ticket2 = TicketType(event_id=1, label='VIP', price=120, quota=20)

db.session.add_all([ticket1, ticket2])
db.session.commit()

print("✅ Ticket types added for event 1")
