from flask import Flask,render_template,url_for,request,session,redirect
from datetime import datetime,date
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:gopireddy@localhost/task1"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = 'my_corpse'
db = SQLAlchemy(app)


# data table1

class Rooms(db.Model):

    __tablename__ = "rooms"
    room_id = db.Column(db.String(20),primary_key = True)
    room_type = db.Column(db.String(40))
    block = db.Column(db.String(10))
    floor = db.Column(db.String(10))
    department = db.Column(db.String(7))

# data table 2

class Rooms_booking(db.Model):

    __tablename__ = "rooms_booking"
    id = db.Column(db.Integer,primary_key = True)
    booking_date = db.Column(db.String(20))
    room_id = db.Column(db.String(20))
    name = db.Column(db.String(10))
    purpose = db.Column(db.String(90))
    phone = db.Column(db.String(15))
    email = db.Column(db.String(50))
    

@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/admin',methods=['POST','GET'])
def admin():
    if request.method == 'POST' :
        admin = str(request.form["admin"])
        if admin == 'pravanya' :
            return redirect('/entry')
        else :
            return render_template('admin.html',mes='Invalid password')
    return render_template('admin.html')

# entering room data into db

@app.route('/entry',methods = ["POST","GET"])
def entry():

    if request.method == "POST":
        room_id = request.form["room"]
        room_type = request.form["roomname"]
        room_type=room_type.upper()
        block = request.form["block"]
        floor = request.form["floor"]
        department = request.form["depart"]

        a=Rooms.query.filter_by(room_id=room_id).first()
        if a is None :
            ad=Rooms(room_id=room_id,room_type=room_type,block=block,floor=floor,department=department)
            db.session.add(ad)
            db.session.commit()
            return render_template('roomsentry.html',mes='room added successfully..!!')
        else :
            return render_template('roomsentry.html',mes='Already room data entered..!!')

    return render_template('roomsentry.html')


# display of all rooms data


@app.route('/allrooms')
def rooms():
    posts=Rooms.query.all()
    return render_template('data.html',posts=posts)


# deleting rooms data in db
        
@app.route('/rooms/delete/<id>')
def delete(id):
    data = Rooms.query.get(id)
    db.session.delete(data)
    db.session.commit()
    return redirect('/allrooms')


# editing or updating roooms data

@app.route('/rooms/edit/<id>',methods =['GET','POST'])
def edit(id):
    data = Rooms.query.get(id)
    if request.method == "POST":
        
        data.room_id = request.form["room"]
        data.room_type = request.form["roomname"]
        data.block = request.form["block"]
        data.floor = request.form["floor"]
        data.department = request.form["depart"]
        db.session.commit()
        return redirect('/allrooms')
    return render_template('editing.html',post=data)

    
# booking with all conditions

@app.route('/booking',methods = ["POST","GET"])
def booking():
    data=Rooms.query.all()
    if request.method == "POST":
        dat = str(request.form["time"])
        room_id = request.form["roomname"]
        name = request.form["name"]
        purpose = request.form["purpose"]
        mobile = request.form["mobile"]
        email = request.form["email"]

        # conforming date
        d=datetime.today()
        l = dat.split('-')
        
        if int(l[2])>d.day and int(l[1])==d.month and int(l[0])>=d.year :
            
            check=Rooms_booking.query.filter_by(booking_date=dat,room_id=room_id).first()
            if check is None :
                bookings = Rooms_booking(booking_date=dat,room_id=room_id,name=name,purpose=purpose,phone=mobile,email=email)
                db.session.add(bookings)
                db.session.commit()
                return render_template('sucess.html',data=bookings)
            else :
                return render_template('roomsbooking.html',data=data,mes='Oops room on that is already booked take another room...!!')

        elif int(l[1])>d.month and int(l[2])<d.day and int(l[0])==d.year :
            check=Rooms_booking.query.filter_by(booking_date=dat,room_id=room_id).first()
            if check is None :
                bookings = Rooms_booking(booking_date=dat,room_id=room_id,name=name,purpose=purpose,phone=mobile,email=email)
                db.session.add(bookings)
                db.session.commit()
                return render_template('sucess.html',data=bookings)
            else :
                return render_template('roomsbooking.html',data=data,mes='Oops room on that is already booked take another room...!!')

        elif int(l[0])>d.year and int(l[2])<d.day and int(l[1])<=d.month :
            print('booking is done by year')
            check=Rooms_booking.query.filter_by(booking_date=dat,room_id=room_id).first()
            if check is None :
                bookings = Rooms_booking(booking_date=dat,room_id=room_id,name=name,purpose=purpose,phone=mobile,email=email)
                db.session.add(bookings)
                db.session.commit()
                return render_template('sucess.html',data=bookings)
            else :
                return render_template('roomsbooking.html',data=data,mes='Oops room on that is already booked choose another room...!!!')
        else :
            return render_template('roomsbooking.html',data=data,mes='Date is invalid plz check...!!!')

    return render_template('roomsbooking.html',data=data)

# showing all bookings

@app.route('/allbookings')
def roomdata():
    d=date.today()
    data=Rooms_booking.query.all()
    l=[]
    for i in data :
        a= i.booking_date
        c = a.split('-')
        if int(c[2])>d.day and int(c[1])==d.month and int(c[0])>=d.year :
            l.append(i)
        elif int(c[1])>d.month and int(c[2])<d.day and int(c[0])==d.year :
            l.append(i)
        elif int(c[0])>d.year and int(c[2])<d.day and int(c[1])<=d.month :
            l.append(i)
        else :
            pass
        
    return render_template('display.html',data=l)

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)