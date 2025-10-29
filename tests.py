from website import create_app, db
from website.models import User, Event, TicketType, Comment, Booking
from datetime import datetime, date, time

app = create_app()

with app.app_context():
    # Clear any existing data
    db.drop_all()
    db.create_all()

    # -------- USERS --------
    user1 = User(
        first_name="Sully",
        last_name="Beare",
        email="sully@example.com",
        password_hash="hashed_pw",  # just a placeholder
    )
    user2 = User(
        first_name="Alice",
        last_name="Wright",
        email="alice@example.com",
        password_hash="hashed_pw",
    )
    db.session.add_all([user1, user2])
    db.session.commit()

    # -------- EVENTS --------
    event1 = Event(
        title="The Life of a Show Girl",
        description=(
            "Lorem ipsum dolor sit amet consectetur adipisicing elit. "
            "Illum vero repellat autem possimus mollitia voluptatum distinctio, "
            "nihil ratione voluptatem animi."
        ),
        genre="Comedy",
        location="Sydney Opera House, Sydney",
        event_date=date(2025, 11, 1),
        start_time=time(19, 0),
        end_time=time(22, 30),
        img="Upcoming1.png",
        status="Open",
        created_by=user1.id,
    )

    event2 = Event(
        title="CTRL",
        description=(
            "Lorem ipsum dolor sit amet consectetur adipisicing elit. "
            "Illum vero repellat autem possimus mollitia voluptatum distinctio, "
            "nihil ratione voluptatem animi."
        ),
        genre="Electronic",
        location="The Tivoli, Brisbane",
        event_date=date(2025, 10, 20),
        start_time=time(19, 0),
        end_time=time(22, 0),
        img="Popular2.png",
        status="Open",
        created_by=user2.id,
    )

    db.session.add_all([event1, event2])
    db.session.commit()

    # -------- TICKET TYPES --------
    t1 = TicketType(event_id=event1.id, label="Standard", price=50.00, quota=200)
    t2 = TicketType(event_id=event1.id, label="VIP", price=120.00, quota=50)
    t3 = TicketType(event_id=event2.id, label="Standard", price=60.00, quota=150)
    db.session.add_all([t1, t2, t3])
    db.session.commit()

    # -------- BOOKINGS --------
    b1 = Booking(user_id=user1.id, ticket_type_id=t2.id, quantity=2)
    b2 = Booking(user_id=user2.id, ticket_type_id=t3.id, quantity=4)
    db.session.add_all([b1, b2])
    db.session.commit()

    # -------- COMMENTS --------
    c1 = Comment(
        content="This event looks awesome!",
        user_id=user1.id,
        event_id=event1.id,
        posted_at=datetime(2025, 10, 20, 6, 1),
    )
    c2 = Comment(
        content="Can’t wait for this show!",
        user_id=user2.id,
        event_id=event1.id,
        posted_at=datetime(2025, 10, 20, 6, 10),
    )
    c3 = Comment(
        content="Such a cool lineup!",
        user_id=user1.id,
        event_id=event2.id,
        posted_at=datetime(2025, 10, 21, 10, 30),
    )
    c4 = Comment(
        content="Booked my tickets already!",
        user_id=user2.id,
        event_id=event2.id,
        posted_at=datetime(2025, 10, 21, 11, 15),
    )
    db.session.add_all([c1, c2, c3, c4])
    db.session.commit()

    print("✅ Sample data created successfully in main.db!")
    print(f"Events: {Event.query.count()} | Users: {User.query.count()} | Bookings: {Booking.query.count()}")
