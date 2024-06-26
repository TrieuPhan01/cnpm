import hashlib

from flask import session
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, Boolean, DateTime, Date, PrimaryKeyConstraint
from sqlalchemy.orm import relationship, backref
from app import db, app, login_manager
from flask_login import UserMixin
import enum

from datetime import datetime
from sqlalchemy import create_engine, engine

from urllib.parse import quote


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    # active = Column(Boolean, default=True)


class UserRoleEnum(enum.Enum):
    USER = 1
    ADMIN = 2
    STAFF = 3


class Staff(BaseModel):
    name = Column(String(20), nullable=False)


# Bảng khách hàng : Thông tin khách hàng đã được lưu chung với user
class User(BaseModel, UserMixin):
    name = Column(String(50), nullable=False)
    passw1 = Column(String(100))
    avatar = Column(String(100),
                    default='https://res.cloudinary.com/dxxwcby8l/image/upload/v1688179242/hclq65mc6so7vdrbp7hz.jpg')
    user_role = Column(Enum(UserRoleEnum), default=UserRoleEnum.USER)
    # receipts = relationship('Receipt', backref='user', lazy=True)
    address = Column(String(100))
    identification = Column(String(20), unique=True, nullable=True)
    email = Column(String(50), nullable=False)
    nationality = Column(String(50))
    birthdate = Column(Date)

    # phone_number = Column(Integer)

    def __str__(self):
        return self.name


# Bảng sân bay
class Airport(BaseModel):
    __tablename__ = 'airport'
    name = Column(String(50), nullable=True)

    def __str__(self):
        return self.name


# Bảng qui định chuyến bay
class Flight_regulations(BaseModel):
    __tablename__ = 'flight_regulations'
    # id = Column(Integer, primary_key=True, autoincrement=True)
    min_onl_ticket_booking_time = Column(Integer, nullable=False)  # thời gian mua vé onl tối thiểu
    min_ticket_sale_time = Column(Integer, nullable=False)  # thời gian bán vé tối thiểu
    min_flight_time = Column(Integer, nullable=False)  # thời gian bay tối thiểu
    minimum_downtime = Column(Integer, nullable=False, default=30)  # thời gian dừng tối thiểu
    maximum_downtime = Column(Integer, nullable=False, default=20)  # thời gian dừng tối da
    current_date = Column(Date)

    def __str__(self):
        return self.min_onl_ticket_booking_time


class Flight_route(BaseModel):
    __tablename__ = 'flight_route'
    departure_airport_id = Column(Integer, ForeignKey(Airport.id))  # 3
    arrival_airport_id = Column(Integer, ForeignKey(Airport.id))  # 4
    bw_airport_id = Column(Integer, ForeignKey(Airport.id))
    name_flight_route = Column(String(50), nullable=False)
    price = Column(Integer, nullable=False)

    ticket_id = relationship('Ticket', backref='flight_route', lazy=False)
    fl_route1 = relationship('Airport', foreign_keys=[departure_airport_id], backref='rule_departure_airport')  # 3
    fl_route2 = relationship('Airport', foreign_keys=[arrival_airport_id], backref='rule_name_flight')  # 3 # 4
    fl_route3 = relationship('Airport', foreign_keys=[bw_airport_id], backref='rule_name_flight_3')

    def __str__(self):
        return self.name_flight_route


# Bảng chuyen bay
class Flight(BaseModel):
    __tablename__ = 'flight'

    # id = Column(Integer, primary_key=True, autoincrement=True)
    flight_regulations_id = Column(Integer, ForeignKey(Flight_regulations.id))  # 2
    number_empty_seats = Column(Integer, nullable=False)
    number_empty_books = Column(Integer)  # Thuộc tính suy diễn !
    time_stop = Column(Integer)
    active = Column(Boolean, default=True)
    deleted = Column(Boolean, default=False)
    number_seats = relationship('Number_of_seats', backref='flight', lazy=False)

    # number_flight = relationship('Flight_Flight_schedule', backref='flight', lazy=False)
    def __str__(self):
        return self.Flight


# Bảng lich bay
class Flight_schedule(BaseModel):
    __tablename__ = 'flight_schedule'
    # id = Column(Integer, primary_key=True, autoincrement=True)
    departure_time = Column(DateTime)  # , nullable=False
    arrival_time = Column(DateTime)  # , nullable=False
    note = Column(String(50))

    # number_schedule = relationship('Flight_Flight_schedule', backref='flight_schedule', lazy=False)

    def __str__(self):
        return self.note


class Flight_Flight_schedule(db.Model):
    flight_id = Column(Integer, ForeignKey(Flight.id), primary_key=True)
    flight_schedule_id = Column(Integer, ForeignKey(Flight_schedule.id), primary_key=True)

    flight = relationship('Flight', backref='flight_flight_schedules')
    flight_schedule = relationship('Flight_schedule', backref='flight_flight_schedules')

    __table_args__ = (
        PrimaryKeyConstraint('flight_id', 'flight_schedule_id'),
    )

    def __str__(self):
        return self.Flight_Flight_schedule


class Flight_route_Flight(db.Model):
    flight_id = Column(Integer, ForeignKey(Flight.id), primary_key=True)
    flight_route_id = Column(Integer, ForeignKey(Flight_route.id), primary_key=True)

    flight = relationship('Flight', backref='flight_flight_route')
    flight_route = relationship('Flight_route', backref='flight_flight_route')

    __table_args__ = (
        PrimaryKeyConstraint('flight_id', 'flight_route_id'),
    )


# class Flight_Flight_schedule(db.Model):
#     __tablename__ = 'Flight_Flight_schedule'
#     flight_id = Column(Integer, ForeignKey(Flight.id), primary_key=True)
#     flight_schedule_id = Column(Integer, ForeignKey(Flight_schedule.id), primary_key=True)
#
#     flight = relationship('Flight', backref='flight_flight_schedules')
#     flight_schedule = relationship('Flight_schedule', backref='flight_flight_schedules')


# Bảng Hạng ghế
class Seat_class(BaseModel):
    __tablename__ = 'seat_class'
    # id = Column(Integer, primary_key=True, autoincrement=True)
    seat_class_name = Column(String(20), nullable=False)
    number_seats = relationship('Number_of_seats', backref='seat_class', lazy=False)

    def __str__(self):
        return self.seat_class_name


# Bảng số lượng ghế
class Number_of_seats(BaseModel):
    __tablename__ = 'Number_of_seats'
    # id = Column(Integer, primary_key=True, autoincrement=True)
    seat_class_id = Column(Integer, ForeignKey(Seat_class.id))
    flight_id = Column(Integer, ForeignKey(Flight.id))
    num = Column(Integer)

    def __str__(self):
        return self.Number_of_seats


# Bảng Hóa đơn
class Bill(BaseModel):
    __tablename__ = 'Bill'
    # id = Column(Integer, primary_key=True, autoincrement=True)
    date_and_time = Column(DateTime, nullable=False)
    Payment_code = Column(String(200), nullable=False)
    ticketb = relationship('Ticket', backref='Bill', lazy=False)

    def __str__(self):
        return self.Bill


# Bảng Loại hành lý
class type_luggage(BaseModel):
    name = Column(String(20), nullable=False)
    weight_max = Column(Integer, nullable=False)

    def __str__(self):
        return self.type_luggage


# Bảng nhân viên quản lý kế thừa bảng nhân viên
class management_staff(Staff):
    management_department = Column(String(30), nullable=False)

    def __str__(self):
        return self.management_staff

    # Bảng Loaị vé


class Ticket_type(BaseModel):
    __tablename__ = 'ticket_type'
    name_Ticket_type = Column(String(60), nullable=False)
    fare_value = Column(Integer, nullable=False)
    tickett = relationship('Ticket', backref='ticket_type', lazy=False)

    def __str__(self):
        return self.Ticket_type


# Bảng Vé
class Ticket(BaseModel):
    __tablename__ = 'ticket'
    # management_department = Column(String(30), nullable=False)
    bill_id = Column(Integer, ForeignKey(Bill.id))  # id hóa đơn
    tick_type_id = Column(Integer, ForeignKey(Ticket_type.id))  # id loại vé
    flightRouter_id = Column(Integer, ForeignKey(Flight_route.id))  # id tuyến bay
    fullName = Column(String(50))
    phoneNumber = Column(String(10))
    email = Column(String(50))
    status = Column(Boolean, nullable=False)

    def __str__(self):
        return self.Ticket


class timve(BaseModel):
    __tablename__ = 'timve'
    ngay_di = Column(String(20))
    san_di = Column(String(20))
    san_den = Column(String(20))

    def __str__(self):
        return self.name


# Viết bên index nó không hiểu. Phải viết qua model nó mới hiểu
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


if __name__ == '__main__':
    with app.app_context():
        # db.create_all()

        a1 = Airport(name='Tân Sơn Nhất')
        a2 = Airport(name="Nội Bài")
        a3 = Airport(name="Côn Đảo")
        a4 = Airport(name="Cà Mau")
        a5 = Airport(name="Cần Thơ")
        a6 = Airport(name="Phú Bài")
        a7 = Airport(name="Vân Đồn")
        a8 = Airport(name="Đà Nẵng")
        a9 = Airport(name="Phú Quốc")
        a10 = Airport(name="Vinh")

        db.session.add_all([a1, a2, a3, a4, a5, a6, a7, a8, a9, a10])
        db.session.commit()

        b1=Flight(number_empty_seats=20,number_empty_books=15,active=1,deleted=0)
        b2=Flight(number_empty_seats=15,number_empty_books=25,active=1,deleted=0)
        b3=Flight(number_empty_seats=19,number_empty_books=16,active=1,deleted=0)
        db.session.add_all([b1, b2, b3])
        db.session.commit()

        g1= Seat_class(seat_class_name='Hạng thương gia')
        g2 = Seat_class(seat_class_name='Hạng thường')
        db.session.add_all([g1, g2])
        db.session.commit()

        a = str(hashlib.md5('123456'.encode('utf-8')).hexdigest())
        d = datetime(2003, 1, 22)
        u = User(name='Hiền Vy', passw1=a, address='Bình Định', identification='333333333311', email='123vy@gmail.com',
                 nationality='Việt Nam', birthdate=d)
        db.session.add(u)
        db.session.commit()

        a11 = str(hashlib.md5('123456'.encode('utf-8')).hexdigest())
        d1 = datetime(2003, 1, 24)
        userR = UserRoleEnum(2)
        u1 = User(name='Hiền Vy admin', passw1=a11, address='Bình Định',user_role=userR, identification='333333333322', email='admin@gmail.com',
                 nationality='Việt Nam', birthdate=d1)
        db.session.add(u1)
        db.session.commit()


        pass
