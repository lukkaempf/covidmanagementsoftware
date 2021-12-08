from . import db
from datetime import datetime, timezone, timedelta
import pytz
from sqlalchemy_utcdatetime import UTCDateTime
from sqlalchemy import DateTime
from flask_login import UserMixin

tz = pytz.timezone('Europe/Berlin')
timenow = datetime.now()
time = timenow + timedelta(hours=-24)

class Seats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seatid = db.Column(db.Integer)
    vorname = db.Column(db.String(50))
    name = db.Column(db.String(50))
    klasse = db.Column(db.String(50))
    email = db.Column(db.String(50))
    #date_created = db.Column(UTCDateTime(tz))
    date_created = db.Column(DateTime(timezone=True), default=time)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'))
    registers = db.relationship('Registers', backref='registerperseat') 
    

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    email = db.Column(db.String(50))
    firstname = db.Column(db.String(50))
    name = db.Column(db.String(50))
    password = db.Column(db.String(200))
    authenticated = db.Column(db.Boolean, default=False)
    isactive = db.Column(db.Boolean, default=True)
    isadmin = db.Column(db.String(10), default=False)
    rooms = db.relationship("Rooms", backref='roomowner')
    


    # def is_active(self):
    #     """True, as all users are active."""
    #     return True

    # def get_id(self):
    #     """Return the username to satisfy Flask-Login's requirements."""
    #     return self.username

    # def is_authenticated(self):
    #     """Return True if the user is authenticated."""
    #     return self.authenticated

    # def is_anonymous(self):
    #     """False, as anonymous users aren't supported."""
    #     return False

class Rooms(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    roomname = db.Column(db.String(50))
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    seats = db.relationship('Seats', backref='seatsinroom')
    qrcodes = db.relationship ('Qrcodes', uselist=False)

""" class Seats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seatnr = db.Column(db.Integer)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'))
    registers = db.relationship('Registers', backref='registerperseat')  """

class Registers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    vorname = db.Column(db.String(50))
    klasse = db.Column(db.String(50))
    email = db.Column(db.String(50))
    dateregisterd = db.Column(DateTime(timezone=True), default=time)
    seats_id = db.Column(db.Integer, db.ForeignKey('seats.id'))

class Qrcodes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    qrcode = db.Column(db.LargeBinary, nullable=False)
    name = db.Column(db.String(50))
    format = db.Column(db.String(20))
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id')) 
    

vorstellung = db.Table('vorstellung',
    db.Column('room_id', db.Integer, db.ForeignKey('rooms.id')),
    db.Column('film_id', db.Integer, db.ForeignKey('film.id'))
)


class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(200))
    roomname= 'default'
    roomid = ''

