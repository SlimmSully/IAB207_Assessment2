from flask import Blueprint
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from . import db
from .models import Event, Comment, TicketType, Booking
from .forms import CommentForm, BookingForm,EventForm,TicketForm
from datetime import datetime
from werkzeug.utils import secure_filename
import os

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    selected_genre = request.args.get('genre')
    genres = [g[0] for g in db.session.query(Event.genre).distinct().all()]
    if selected_genre:
        events = Event.query.filter_by(genre=selected_genre).all()
    else:
        events = Event.query.all()
    carousel_events = Event.query.order_by(db.func.random()).limit(3).all()
    return render_template('index.html', events=events, genres=genres,
                           selected_genre=selected_genre, carousel_events=carousel_events)

from flask import request

@main_bp.route('/search')
def search():
    query = request.args.get('q', '')
    if query:
        # Search title or description (case-insensitive)
        events = Event.query.filter(
            Event.title.ilike(f'%{query}%') | Event.description.ilike(f'%{query}%')
        ).all()
    else:
        events = []
    return render_template('search_results.html', events=events, query=query)


# Event detail view with comments and booking
@main_bp.route('/event/<int:event_id>', methods=['GET', 'POST'])
def event_detail(event_id):
    
    event = Event.query.get_or_404(event_id)
    comments = Comment.query.filter_by(event_id=event_id).order_by(Comment.posted_at.desc()).all()
    ticket_types = TicketType.query.filter_by(event_id=event.event_id).all()
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
            user_id=current_user.user_id,
            event_id=event.event_id,
            posted_at=datetime.now()
        )
        db.session.add(new_comment)
        db.session.commit()
        flash('Comment posted successfully!', 'success')
        return redirect(url_for('main.event_detail', event_id=event.event_id))

    # booking submission
    elif booking_form.validate_on_submit() and booking_form.submit.data:
        if not current_user.is_authenticated:
            flash('You must be logged in to book tickets.', 'warning')
            return redirect(url_for('auth.login'))

        ticket_type_id = booking_form.ticket_type.data
        quantity = booking_form.ticket_quantity.data
        ticket_type = TicketType.query.get(ticket_type_id)

        new_booking = Booking(
            user_id=current_user.user_id,
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

    return render_template('bookingconfirmation.html', booking=booking, ticket_type=ticket_type, event=event, user=user)

# booking history page
@main_bp.route("/bookinghistory")
#@login_required
def booking_history():
    
    bookings = (
        db.session.query(Booking, TicketType, Event)
        .join(TicketType, Booking.ticket_type_id == TicketType.ticket_type_id)
        .join(Event, Event.event_id == TicketType.event_id)
        #.filter(Booking.user_id == current_user.user_id)
        .all()
    )

    return render_template("bookinghistory.html", bookings=bookings)


@main_bp.route("/CreateEvent", methods=["GET", "POST"])
def CreateEvent():
    form = EventForm()

    if form.validate_on_submit():
        img_file = request.files.get("img_file")
        filename = "default.jpeg"

        if img_file and img_file.filename != "":
            filename = secure_filename(img_file.filename)
            save_path = os.path.join("website", "static", "img", filename)
            img_file.save(save_path)
            
        ev = Event(
            title=form.title.data.strip(),
            genre=form.genre.data,
            description=form.description.data.strip(),
            location=form.location.data.strip() if form.location.data else None,
            event_date=form.event_date.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data,
            img=filename or "default.jpeg",
            status="Open",
            created_by=getattr(current_user, "user_id", None)
        )
        db.session.add(ev)
        db.session.commit() 

        ticket_labels = request.form.getlist("ticket_label[]")
        ticket_prices = request.form.getlist("ticket_price[]")
        ticket_quotas = request.form.getlist("ticket_quota[]")

        for label, price, quota in zip(ticket_labels, ticket_prices, ticket_quotas):
            ticket = TicketType(
                event_id=ev.event_id,      
                label=label,
                price=float(price),
                quota=int(quota)
            )
            db.session.add(ticket)
        db.session.commit()

        flash("Event & ticket types created successfully!", "success")
        return redirect(url_for("main.index", event_id=ev.event_id))
    return render_template("CreateEvent.html", form=form)



@main_bp.route("/EditEvent/<int:event_id>", methods=["GET", "POST"])
def EditEvent(event_id):
    ev = Event.query.get_or_404(event_id)
    form = EventForm(obj=ev)

    ticket_types = TicketType.query.filter_by(event_id=event_id).all()

    if form.validate_on_submit():            
        ev.title = form.title.data
        ev.genre = form.genre.data
        ev.description = form.description.data
        ev.location = form.location.data
        ev.event_date = form.event_date.data
        ev.start_time = form.start_time.data
        ev.end_time = form.end_time.data
        ev.status = request.form.get("status")

        img_file = request.files.get("img_file")
        if img_file and img_file.filename != "":
            filename = secure_filename(img_file.filename)
            save_path = os.path.join("website", "static", "img", filename)
            img_file.save(save_path)
            ev.img = filename 

        TicketType.query.filter_by(event_id=event_id).delete()

        ticket_labels = request.form.getlist("ticket_label[]")
        ticket_prices = request.form.getlist("ticket_price[]")
        ticket_quotas = request.form.getlist("ticket_quota[]")

        for label, price, quota in zip(ticket_labels, ticket_prices, ticket_quotas):
            db.session.add(TicketType(
                event_id=event_id,
                label=label,
                price=float(price),
                quota=int(quota)
            ))

        db.session.commit()
        flash("Event updated successfully!", "success")
        return redirect(url_for("main.event_detail", event_id=event_id))

    return render_template("EditEvent.html", form=form, event=ev, ticket_types=ticket_types)

