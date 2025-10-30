from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, SelectField, IntegerField, FileField, RadioField, DateField, DateTimeField, TimeField
from wtforms.validators import InputRequired, Length, Email, EqualTo, DataRequired, NumberRange, Optional

# creates the login information
class LoginForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired('Enter user name')])
    password  = PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit    = SubmitField("Login")

# this is the registration form
class RegisterForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired()])
    email = StringField("Email Address",validators=[InputRequired(), Length(max=120)],filters=[lambda x: x.strip() if x else x],)
    # linking two fields - password should be equal to data entered in confirm
    password  = PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match")])
    confirm   = PasswordField("Confirm Password")
    first_name = StringField("First Name", validators=[InputRequired(), Length(max=50)])
    last_name  = StringField("Surname",    validators=[InputRequired(), Length(max=50)])
    phone      = StringField("Contact Number", validators=[Optional(), Length(max=20)])
    address    = StringField("Street Address",  validators=[Optional(), Length(max=200)])

    # submit button
    submit    = SubmitField("Register")

# form for adding comments on event details page
class CommentForm(FlaskForm):
    content = TextAreaField('Write a comment', validators=[InputRequired(), Length(max=500)])
    submit  = SubmitField('Post Comment')

# form for booking tickets
class BookingForm(FlaskForm):
    ticket_type = SelectField('Ticket Type', coerce=int, validators=[DataRequired()])
    ticket_quantity = IntegerField(
        'Number of Tickets',
        validators=[DataRequired(), NumberRange(min=1, max=10)]
    )
    submit = SubmitField('Book Now')

class EventForm(FlaskForm):
    title       = StringField("Title", validators=[DataRequired()])
    genre       = SelectField("Genre", choices=[
        ("Hip Hop","Hip Hop"), ("R&B","R&B"), ("Jazz","Jazz"),
        ("Rap","Rap"), ("Electronic","Electronic"), ("Comedy","Comedy")
    ], validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    location    = StringField("Location", validators=[DataRequired()])
    event_date  = DateField("Date", format="%Y-%m-%d", validators=[DataRequired()])
    start_time  = TimeField("Start time", format="%H:%M", validators=[DataRequired()])
    end_time    = TimeField("End time", format="%H:%M")
    img         = FileField("Upload Image")
    submit      = SubmitField("Save event")

class TicketForm(FlaskForm):
    Label = StringField("Ticket Type", validators=[InputRequired()])
    Price = IntegerField("Price", validators=[InputRequired()])
    Quota = IntegerField("quota for profit")
