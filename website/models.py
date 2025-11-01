# website/models.py
from . import db
from datetime import datetime, date
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# USER MODEL
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # relationships
    comments = db.relationship('Comment', backref='user', lazy=True)
    events = db.relationship('Event', backref='creator', lazy=True)
    
    def get_id(self):
        return str(self.user_id)

    # password utilities
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.first_name} {self.last_name}>'

# EVENT MODEL
class Event(db.Model):
    __tablename__ = 'events'

    event_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    genre = db.Column(db.String(50))
    location = db.Column(db.String(150))
    event_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    img = db.Column(db.String(200))
    status = db.Column(db.String(20), default='Open') 
    created_by = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    created_at = db.Column(db.DateTime, default=datetime.now)

    # relationships
    comments = db.relationship('Comment', backref='event', lazy=True)

    def __repr__(self):
        return f'<Event {self.title}>'
    
    def update_status_if_inactive(self):
        # set status to 'Inactive' if the event date is in the past
        if self.event_date and self.event_date < date.today() and self.status not in ['Cancelled']:
            self.status = 'Inactive'
            db.session.commit()

# COMMENT MODEL
class Comment(db.Model):
    __tablename__ = 'comments'

    comment_id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    posted_at = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id'), nullable=False)

    def __repr__(self):
        return f'<Comment {self.user_id} by User {self.user_id} on Event {self.event_id}>'
    

# TICKET TYPE MODEL
class TicketType(db.Model):
    __tablename__ = 'ticket_types'

    ticket_type_id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id'), nullable=False)
    label = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quota = db.Column(db.Integer)

    event = db.relationship('Event', backref=db.backref('ticket_types', lazy=True))

    def __repr__(self):
        return f'<TicketType {self.label} - ${self.price}>'

# BOOKING MODEL
class Booking(db.Model):
    __tablename__ = 'bookings'

    booking_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    ticket_type_id = db.Column(db.Integer, db.ForeignKey('ticket_types.ticket_type_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    booked_at = db.Column(db.DateTime, default=datetime.now)

    user = db.relationship('User', backref='bookings', lazy=True)
    ticket_type = db.relationship('TicketType', backref='bookings', lazy=True)

    def __repr__(self):
        return f'<Booking user={self.user_id}, ticket={self.user_id}, qty={self.quantity}>'
    
    def get_id(self):
        return str(self.user_id)

