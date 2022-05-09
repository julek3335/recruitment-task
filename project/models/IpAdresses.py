from . import db, ma

class IpAdresses(db.Model):
    __tablename__ = 'ipAdresses'
    _id = db.Column("id", db.Integer, primary_key = True)
    ip = db.Column(db.String(45))

    def __init__(self, ip):
        self.ip = ip

    def db_save(self):
        db.session.add(self)
        db.session.commit()