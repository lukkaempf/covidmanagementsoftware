from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from .models import Seats, Users, Rooms, Registers, Qrcodes, Film, vorstellung
from . import db
from datetime import datetime, timedelta
import pytz
from flask_login import login_user, login_required, logout_user, current_user
import json
import requests
from werkzeug.utils import secure_filename
import base64
from sqlalchemy import insert

views= Blueprint('views', __name__)
i = ''
tz = pytz.timezone('Europe/Berlin')
blockedseat2 = ''



def test(seatid):
    lastitemwithid = Seats.query.filter_by(seatid=seatid).order_by(Seats.id.desc()).first()
    oldtime2 = lastitemwithid.date_created
    print(oldtime2)
    #currenttime = datetime.now(tz)
    currenttime2 = datetime.now()
    print(currenttime2)
    currenttime122 = currenttime2 + timedelta(hours=-12)
    print(currenttime122)
    if currenttime122 < oldtime2:
        global blockedseat2
        blockedseat2 = True    
    else:
        blockedseat2 = False

@views.route('/')
def home():
    user  = current_user

    allFilms = db.session.query(Film).all()
    for film in allFilms:
        room=db.session.query(Rooms).join(vorstellung).filter_by(film_id=film.id).first()   
        film.roomname=room.roomname
        film.roomid=room.id
    return render_template('home.html', user=user, allFilms=allFilms)


@views.route('/oldhome', methods=['POST','GET'])
def oldhome():
    seats = Seats.query.order_by(Seats.seatid).all()
    print(seats)
    aa = {}
   
    for seat in seats:
        print(seat.seatid)

        test(seat.seatid)
        aa[seat.seatid] = blockedseat2
        
        print(blockedseat2)
    print(aa)
    return render_template('oldhome.html', seats=seats,blockedseat=blockedseat2, aa=aa)

@views.route('/seat/<int:seatid>', methods=['GET', 'POST'])
def seat(seatid):
    acceptrequret = False
    test(seatid)
    if blockedseat2 == True:
        return 'hello' 
    else:
        if request.method=='POST':
            vorname = request.form['vorname']
            name = request.form['name']
            klasse = request.form['klasse']
            email = request.form['email']
            accept = request.form.getlist('check')
            if accept:
                print(vorname, name, klasse, email, accept)
                currendtime = datetime.now(tz)
                
                registerseat = Seats(seatid=seatid, vorname=vorname, name=name, klasse=klasse, email=email, date_created=currendtime)
                try:
                    db.session.add(registerseat)
                    db.session.commit()
                except:
                    print('Datenbankfehler')
                return redirect (url_for(".confirm" , seatid=seatid))
            else:
                acceptrequret = True
        return render_template('seat.html', acceptrequret=acceptrequret)

@views.route('/seat/<int:seatid>/confirm')
def confirm(seatid):
    seatconfirm = Seats.query.filter_by(seatid=seatid).order_by(Seats.id.desc()).first()
    return render_template('seatconfirm.html', seatconfirm=seatconfirm)



@views.route('/create')
def create_seats():
    for i in range(1,31):
        exists = Seats.query.filter_by(seatid=i).first()
        if not exists:
            seats_to_create = Seats(seatid=i)
            db.session.add(seats_to_create)
            db.session.commit()
            print('Success')
    return 'test'

@views.route('/login/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = Users.query.filter_by(username = username).first()

        if current_user.is_authenticated:
            return redirect(url_for('.admin'))
    
        if user:
            if password == user.password:
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                print(user)
                login_user(user, remember=True)
                print(current_user)
                print(current_user.is_authenticated )
                return redirect (url_for('.admin'))
            else:
                print('Login fehlgeschlagen')
        else:
            print('Benutzername nicht vorhanden')
    return render_template('login.html')

@views.route('/logout/')
@login_required
def logout():
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return redirect (url_for('.home'))

@views.route('/signup/', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        firstname = request.form['firstname']
        name = request.form['name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        user = Users.query.filter_by(username = username).first()
        
        if user:
            print('Benutzer existiert bereits')
        else:
            newuser = Users(firstname=firstname, name=name, email=email, username=username, password=password)
            try:
                db.session.add(newuser)
                db.session.commit()


                print('Neuer User erstellt')
                return redirect (url_for('.login'))
            except:
                print('Datenbank Fehler')
    return render_template('signup.html')

@views.route('/admin/', methods=['GET','POST'])
@login_required
def admin():
    user  = current_user
    return render_template('/admin.html', user=user)

@views.route('/rooms/', methods=['GET','POST'])
@login_required
def rooms():
    user  = current_user
    rooms = db.session.query(Rooms).all()
    return render_template('/admin_rooms.html', user=user, rooms=rooms)

@views.route('/danke/', methods=['GET','POST'])
def danke():
    user  = current_user
    return render_template('/danke.html', user=user)

@views.route('/admin/updateroomname', methods=['GET','POST'])
def updateroomname():
    room = json.loads(request.data)
    print(room['roomid'])
    print(room)
    roomdb = Rooms.query.get(room['roomid'])
    roomdb.roomname = room['newname']
    db.session.commit()
    return jsonify({roomdb})

@views.route('/admin/deleteroom', methods=['GET','POST'])
def deleteroom():
    roomidtodelete = json.loads(request.data)
    roomtodelete = Rooms.query.get(roomidtodelete['roomid'])
    if roomtodelete:
        if roomtodelete.users_id == current_user.id:
            db.session.delete(roomtodelete)
            db.session.commit()
        else:
            print('Nur der Besitzer des Raums ist zum löschen berechtigt.')
    return jsonify ({})

@views.route('/admin/newroom', methods=['GET','POST'])
def newroom():
    roomtocreate = json.loads(request.data)
    if roomtocreate:
        newroom = Rooms(roomname=roomtocreate['newname'], sumseats=roomtocreate['sumseats'], users_id=current_user.id)
        db.session.add(newroom)
        db.session.commit()
        #URL TO REQUEST AND FILE COLUMNS WITH THE RIGHT STUFF
        url = "https://testing.llic.ch/admin/"+str(newroom.id)+"/register"
        print(url)
        r = requests.get("http://api.qrserver.com/v1/create-qr-code/?data="+url+"&size=600x600")
        newqrcode = Qrcodes(qrcode=r.content, name="qrcode_"+newroom.roomname, format="png", room_id=newroom.id)
        db.session.add(newqrcode)
        db.session.commit()
    return jsonify ({})

@views.route('/admin/<int:roomid>/options/')
def roomoptions(roomid):
    room = Rooms.query.get(roomid)
    qrcode = db.session.query(Qrcodes).filter(Qrcodes.room_id==roomid).first()
    if qrcode:
        image = base64.b64encode(qrcode.qrcode).decode("utf-8")
    else:
        return "API need Network"
    return render_template('admin_roomoptions.html', room=room, image=image)

@views.route('/admin/register/<int:roomid>/', methods=['GET','POST'])
def register(roomid):
    room = Rooms.query.get(roomid)
    data = request.form
    if data:
        newregister = Registers(vorname=data['vorname'],name=data['name'],seatnr=data['seatnr'],email=data['email'],roomid=roomid)
        db.session.add(newregister)
        db.session.commit()
    return render_template('register.html', room=room)

@views.route('/admin/taken/<int:roomid>/')
def taken(roomid):
    room = Rooms.query.get(roomid)
    registers = db.session.query(Registers).filter(roomid==roomid).all()
    currenttime12h = datetime.now() + timedelta(hours=-12)
    """ print(currenttime12h)
    for seat in seatinfos:
        print(seat.registers[0].dateregisterd)
        print(seat.seatnr,seat.registers[0].name,seat.registers[0].vorname,seat.registers[0].klasse)
        if seat.registers[0].dateregisterd > currenttime12h:
            print('Sitz ist Frei')
        else:
            print('Sitz ist besetzt') """
    return render_template('taken.html', room=room, registers=registers, currenttime12h=currenttime12h)

@views.route('/admin/taken/<int:roomid>/history/<int:seatnr>/')
def history(roomid,seatnr):
    room = Rooms.query.get(roomid)
    registers = db.session.query(Registers).filter(seatnr==Registers.seatnr,roomid==roomid).all()
    return render_template('history.html', registers=registers)
    


@views.route('/admin/user/', methods=['GET','POST','DELETE','UPDATE'])
@login_required
def user():
    allUsers = db.session.query(Users).all()

    if request.method=='POST':
        usertocreate = json.loads(request.data)
        print(usertocreate)
        if usertocreate['username']:
            newuser = Users(username=usertocreate['username'], firstname=usertocreate['firstname'], name=usertocreate['name'],password=usertocreate['password'],isadmin=usertocreate['isadmin'])
            db.session.add(newuser)
            db.session.commit()
            return render_template('admin_users.html') 
    if request.method=='DELETE':
        usertodelete = json.loads(request.data)
        useridtodelete = json.loads(request.data)
        usertodelete = Users.query.get(useridtodelete['userid'])
        if usertodelete:
            db.session.delete(usertodelete)
            db.session.commit()
    if request.method=='UPDATE':
        usertoupdate = json.loads(request.data)
        print(usertoupdate)
        dbusertoupdate = Users.query.get(usertoupdate['userid'])
        dbusertoupdate.username = usertoupdate['updateusername']
        dbusertoupdate.firstname = usertoupdate['updatefirstname']
        dbusertoupdate.name = usertoupdate['updatename']
        dbusertoupdate.password = usertoupdate['updatepassword']
        dbusertoupdate.isadmin = usertoupdate['updateisadmin']
        db.session.commit()
    return render_template('admin_users.html', allUsers=allUsers)  
   

@views.route('/admin/film/', methods=['GET','POST','DELETE','UPDATE'])
@login_required
def films():
    user  = current_user
    allFilms = db.session.query(Film).all()
    for film in allFilms:
        room=db.session.query(Rooms).join(vorstellung).filter_by(film_id=film.id).first()   
        film.roomname=room.roomname
        film.roomid=room.id
    if request.method == 'POST':
        filmtoadd = json.loads(request.data)
        room = db.session.query(Rooms).filter_by(roomname=filmtoadd['roomname']).first()
        if room:
            newFilm = Film(name=filmtoadd['name'], description=filmtoadd['description'])
            db.session.add(newFilm)
            db.session.commit()
            #INSERT INTO LINKTABLE
            print(newFilm.id, room.id)
            newFilm_Room = vorstellung.insert().values(room_id=room.id,film_id=newFilm.id)
            db.session.execute(newFilm_Room)
            db.session.commit() 
            print('success')
        else:
            print('Saalname wurde nicht gefunden')
    if request.method=='UPDATE':
        filmtoupdate = json.loads(request.data)
        dbfilmtoupdate = Film.query.get(filmtoupdate['filmid'])
        dbfilmtoupdate.name = filmtoupdate['name']
        dbfilmtoupdate.description = filmtoupdate['description']
        dbfilmtoupdate.roomname = filmtoupdate['roomname']
        db.session.commit()
    if request.method=='DELETE':
        filmidtodelete = json.loads(request.data)
        filmtodelete = Film.query.get(filmidtodelete['filmid'])
        print(filmidtodelete['filmid'])
        db.session.query(vorstellung).filter_by(film_id=filmidtodelete['filmid']).delete()
        db.session.delete(filmtodelete)
        db.session.commit()

    return render_template('/admin_films.html', user=user, allFilms=allFilms)


@views.route('/test/')
def test():
    return render_template('/test.html')