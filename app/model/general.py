from app.extensions import db

class PriorityCriteria(db.Model):
    __tablename__="priority_criteria"
    id = db.Column(db.BIGINT, primary_key=True)
    description = db.Column(db.String(100), nullable=False)

class Type(db.Model):
    __tablename__="type"
    id = db.Column(db.BIGINT, primary_key=True)
    parent_type = db.Column(db.String(100), nullable=False)
    value = db.Column(db.String(250), nullable=False)

class Area(db.Model):
    __tablename__="area"
    id = db.Column(db.BIGINT, primary_key=True)
    name = db.Column(db.String(50), nullable=False)