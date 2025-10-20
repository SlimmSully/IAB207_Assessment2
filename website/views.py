from flask import Blueprint
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from . import db
from .models import Event, Comment, TicketType, Booking
from .forms import CommentForm, BookingForm
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return '<h1>Starter code for assignment 3<h1>'

# Event detail view with comments and booking
@main_bp.route('/event/<int:event_id>', methods=['GET', 'POST'])
def event_detail(event_id):
    # ----------------------------------------------------- DELETE LATER
    # temporarily simulate user 1 being logged in 
    from .models import User
    from flask_login import login_user
    fake_user = User.query.first()
    if fake_user:
        login_user(fake_user)
    # ----------------------------------------------------- DELETE LATER

    event = Event.query.get_or_404(event_id)
    comments = Comment.query.filter_by(event_id=event.id).order_by(Comment.posted_at.desc()).all()
    ticket_types = TicketType.query.filter_by(event_id=event.id).all()
    booking_message = None

    # create both forms
    comment_form = CommentForm()
    booking_form = BookingForm()

    # populate ticket type choices dynamically
    booking_form.ticket_type.choices = [
        (t.ticket_type_id, f"{t.label} - ${t.price:.2f}") for t in ticket_types
    ]

    booking_message = None

    # comment submission
    if comment_form.validate_on_submit() and comment_form.submit.data:
        if not current_user.is_authenticated:
            flash('You must be logged in to post a comment.', 'warning')
            return redirect(url_for('auth.login'))

        new_comment = Comment(
            content=comment_form.content.data,
            user_id=current_user.id,
            event_id=event.id,
            posted_at=datetime.utcnow()
        )
        db.session.add(new_comment)
        db.session.commit()
        flash('Comment posted successfully!', 'success')
        return redirect(url_for('main.event_detail', event_id=event.id))

    # booking submission
    elif booking_form.validate_on_submit() and booking_form.submit.data:
        if not current_user.is_authenticated:
            flash('You must be logged in to book tickets.', 'warning')
            return redirect(url_for('auth.login'))

        ticket_type_id = booking_form.ticket_type.data
        quantity = booking_form.ticket_quantity.data
        ticket_type = TicketType.query.get(ticket_type_id)

        new_booking = Booking(
            user_id=current_user.id,
            ticket_type_id=ticket_type_id,
            quantity=quantity
        )
        db.session.add(new_booking)
        db.session.commit()

        return redirect(url_for('main.booking_confirmation', booking_id=new_booking.booking_id))

    # render template
    return render_template('details.html', event=event, comments=comments, comment_form=comment_form, booking_form=booking_form, booking_message=booking_message)


# booking confirmation page
@main_bp.route('/booking/<int:booking_id>/confirmation')
def booking_confirmation(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    ticket_type = booking.ticket_type
    event = ticket_type.event
    user = booking.user

    return render_template(
        'bookingconfirmation.html',
        booking=booking,
        ticket_type=ticket_type,
        event=event,
        user=user
    )
