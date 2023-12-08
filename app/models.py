import datetime
from app import db
from sqlalchemy.sql import func

class Deploy(db.Model):
    __tablename__ = "record"

    id = db.Column(db.Integer, primary_key=True)
    host = db.Column(db.String(1000), nullable=False)
    username = db.Column(db.String(1000), nullable=False)
    password = db.Column(db.String(800),  nullable=False)
    dbnames = db.Column(db.String(800),  nullable=False)
    tool = db.Column(db.String(800),  nullable=False)
    status = db.Column(db.String(800),  nullable=False)
    isActive = db.Column(db.String(800), nullable=False)
    expiry = db.Column(db.String(800), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())

    def __init__(
        self, host, username, password, dbnames, tool, status, expiry, created_at, 
    ):
        self.host = host
        self.username = username
        self.password = password
        self.dbnames = dbnames
        self.tool = tool
        self.status = status
        self.expiry = expiry
        self.created_at = created_at

