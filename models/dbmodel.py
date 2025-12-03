from app import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint
from werkzeug.security import generate_password_hash
from datetime import datetime 
import os

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'

    user_id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    email_id = db.Column(db.String(50), unique=True, nullable=False)
    pass_wd = db.Column(db.String(100), nullable=False)
    user_name = db.Column(db.String(50), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    bookings = db.relationship('UserBookings', backref='user', cascade="all, delete-orphan", passive_deletes=True)
    history = db.relationship('UserHistory', backref='user', cascade="all, delete-orphan", passive_deletes=True)
    notifications = db.relationship('UserNotification', backref='user', cascade="all, delete-orphan", passive_deletes=True)


class UserBookings(db.Model):
    __tablename__ = 'user_bookings'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id", ondelete="CASCADE"), nullable=False)
    spot_id = db.Column(db.Integer, db.ForeignKey("parking_spot.spot_id", ondelete="CASCADE"), nullable=False)
    parking_time = db.Column(db.DateTime, nullable=False)
    leaving_time = db.Column(db.DateTime, nullable=False)
    parking_cost = db.Column(db.Numeric(7, 2), nullable=False)
    vehicle_no = db.Column(db.String(12), nullable=False)

    spot = db.relationship('ParkingSpot', back_populates='bookings')


class UserHistory(db.Model):
    __tablename__ = 'booking_history'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id", ondelete="CASCADE"), nullable=False)
    spot_id = db.Column(db.Integer, db.ForeignKey("parking_spot.spot_id", ondelete="SET NULL"), nullable=True)
    booking_time = db.Column(db.DateTime, nullable=False)
    leaving_time = db.Column(db.DateTime, nullable=False)
    parking_cost = db.Column(db.Numeric(7, 2), nullable=False)
    vehicle_no = db.Column(db.String(12), nullable=False)

    spot_obj = db.relationship('ParkingSpot', back_populates='history_records')


class ParkingLot(db.Model):
    __tablename__ = 'parkinglot'

    lot_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    area_type = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    primelocation_name = db.Column(db.String(100), nullable=False)
    price_per_hr = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(200), unique=True, nullable=False)
    pincode = db.Column(db.String(6), nullable=False)

    spots = db.relationship('ParkingSpot', backref='lot', cascade="all, delete-orphan", passive_deletes=False)

    __table_args__ = (
        db.CheckConstraint("area_type IN ('Open','Covered','Both')", name='check_area_type'),
    )


class ParkingSpot(db.Model):
    __tablename__ = 'parking_spot'

    spot_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    lot_id = db.Column(db.Integer, db.ForeignKey("parkinglot.lot_id"), nullable=False)
    status = db.Column(db.String(1), nullable=False) # O-occupied, A-available

    bookings = db.relationship('UserBookings', back_populates='spot', passive_deletes=True)
    history_records = db.relationship('UserHistory', back_populates='spot_obj', passive_deletes=True)

    __table_args__ = (
        CheckConstraint("status IN ('O','A')", name='check_status_occupied'),
    )


class UserNotification(db.Model):
    __tablename__ = 'user_notifications'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete="CASCADE"), nullable=False)
    message_category = db.Column(db.String(50), nullable=False) # e.g., 'info', 'warning', 'success', 'danger'
    message_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    is_read = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"<UserNotification {self.id} User:{self.user_id} Category:{self.message_category} Read:{self.is_read}>"


with app.app_context():
    db_uri = app.config.get('SQLALCHEMY_DATABASE_URI')            #get dbfile configured path in app config like 'sqlite///filename'
    db_filename = db_uri.replace('sqlite:///', '')
    #remove "sqlite:///" from fetched configured path so just filename
    db_file_path = os.path.join(app.instance_path, db_filename)   #join with file name with root folder/instance/filename
    db_existed_bef_create_all = os.path.exists(db_file_path)      #check if a files exists in that path 
    #print(f"DEBUG: checking for DB file at: {db_file_path}")     #to debug, showed correct behaviour therefore commented
    db.create_all()

    # -------------------- create Master User Admin (only if not exists) ----------------------
    admin_email = "parkalot@admin"
    admin_password = "1234"
    admin_username = "Admin"
    
    # Check if the admin user already exists
    existing_admin = User.query.filter_by(is_admin=True).first()

    if not existing_admin:
        passhash = generate_password_hash(admin_password)
        master_admin = User(user_id=1, email_id=admin_email, pass_wd=passhash, user_name=admin_username, is_admin=True)
        db.session.add(master_admin)
        db.session.commit()
        print(f"Master Admin user '{admin_username}' ({admin_email}) created successfully with ID 1.")
    else:
        print(f"Master Admin user '{admin_email}' already exists. Skipping creation.")


    # ---------------------- Populate dummy parking lot data, only add if new db/tables created --------------------

    if not db_existed_bef_create_all:
        print("Populating dummy parking lot data...")
        
        # all parkinglots data nested list of dictionaries
        dummy_parking_lots_data = [
            {"area_type": "Open", "city": "Mumbai", "primelocation_name": "Gateway Gardens", "price_per_hr": 60.0, "address": "101 Marine Drive, Mumbai", "pincode": "400001"},
            {"area_type": "Covered", "city": "Delhi", "primelocation_name": "Connaught Place Hub", "price_per_hr": 55.0, "address": "202 Barakhamba Rd, Delhi", "pincode": "110001"},
            {"area_type": "Both", "city": "Noida", "primelocation_name": "Sector 18 Plaza", "price_per_hr": 45.0, "address": "303 Main Rd, Noida", "pincode": "201301"},
            {"area_type": "Open", "city": "Gurugram", "primelocation_name": "Cyber City Parking", "price_per_hr": 50.0, "address": "404 Cyber Hub, Gurugram", "pincode": "122001"},
            {"area_type": "Covered", "city": "Bangalore", "primelocation_name": "MG Road Garage", "price_per_hr": 70.0, "address": "505 MG Rd, Bangalore", "pincode": "560001"},
            {"area_type": "Open", "city": "Pune", "primelocation_name": "Deccan Gymkhana Lot", "price_per_hr": 35.0, "address": "606 FC Rd, Pune", "pincode": "411004"},
            {"area_type": "Both", "city": "Hyderabad", "primelocation_name": "Hitech City Towers", "price_per_hr": 50.0, "address": "707 Mindspace, Hyderabad", "pincode": "500081"},
            {"area_type": "Open", "city": "Chennai", "primelocation_name": "Besant Nagar Beach", "price_per_hr": 40.0, "address": "808 Beach Rd, Chennai", "pincode": "600090"},
            {"area_type": "Covered", "city": "Ahmedabad", "primelocation_name": "Sabarmati Riverfront", "price_per_hr": 30.0, "address": "909 Riverfront East, Ahmedabad", "pincode": "380001"},
            {"area_type": "Open", "city": "Jaipur", "primelocation_name": "Pink City Bazaar", "price_per_hr": 38.0, "address": "1010 Hawa Mahal Rd, Jaipur", "pincode": "302002"},
            {"area_type": "Both", "city": "Kolkata", "primelocation_name": "Park Street Hub", "price_per_hr": 42.0, "address": "1111 Park St, Kolkata", "pincode": "700016"},
            {"area_type": "Open", "city": "Indore", "primelocation_name": "Rajwada Palace Lot", "price_per_hr": 25.0, "address": "1212 MG Rd, Indore", "pincode": "452001"},
            {"area_type": "Covered", "city": "Bhopal", "primelocation_name": "Upper Lake Parking", "price_per_hr": 28.0, "address": "1313 Lake View Rd, Bhopal", "pincode": "462001"},
            {"area_type": "Open", "city": "Lucknow", "primelocation_name": "Hazratganj Market", "price_per_hr": 30.0, "address": "1414 Ganj Rd, Lucknow", "pincode": "226001"},
            {"area_type": "Both", "city": "Chandigarh", "primelocation_name": "Sector 17 Plaza", "price_per_hr": 38.0, "address": "1515 Sector 17, Chandigarh", "pincode": "160017"},
            {"area_type": "Open", "city": "Kochi", "primelocation_name": "Fort Kochi Parking", "price_per_hr": 32.0, "address": "1616 Fort Rd, Kochi", "pincode": "682001" }
            ]

        for lot_data in dummy_parking_lots_data:
            new_lot = ParkingLot(
                area_type=lot_data["area_type"],
                city=lot_data["city"],
                primelocation_name=lot_data["primelocation_name"],
                price_per_hr=lot_data["price_per_hr"],
                address=lot_data["address"],
                pincode=lot_data["pincode"])
            
            db.session.add(new_lot)
            db.session.flush() # get lot_id before commit

            # add 10 spots for each lot
            for _ in range(10):
                db.session.add(ParkingSpot(lot_id=new_lot.lot_id, status='A'))
            
        db.session.commit()
        print("Dummy parking lot data populated.")
    else:
        print("Parking lot data already exists. Skipping dummy data population.")
