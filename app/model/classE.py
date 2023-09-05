from app.extensions import db

class Class(db.Model):
    __tablename__="class"
    id = db.Column(db.BIGINT, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    space_capacity = db.Column(db.Integer, nullable=False)
    

class CharacteristicClass(db.Model):
    __tablename__="class_characteristic"
    id = db.Column(db.BIGINT, primary_key=True)
    name = db.Column(db.String(200), nullable=False)

class ClassCharacteristic(db.Model):
    __tablename__="characteristic_class"
    id = db.Column(db.BIGINT, primary_key=True)
    class_id = db.Column(db.BIGINT, db.ForeignKey('class.id'))
    characteristic_id = db.Column(db.BIGINT, db.ForeignKey('class_characteristic.id'))

class ClassOP(db.Model):
    __tablename__="class_op"
    id = db.Column(db.BIGINT, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    space_capacity = db.Column(db.Integer, nullable=False)
    

class CharacteristicClassOP(db.Model):
    __tablename__="class_characteristic_op"
    id = db.Column(db.BIGINT, primary_key=True)
    name = db.Column(db.String(200), nullable=False)

class ClassCharacteristicOP(db.Model):
    __tablename__="characteristic_class_op"
    id = db.Column(db.BIGINT, primary_key=True)
    class_id = db.Column(db.BIGINT, db.ForeignKey('class_op.id'))
    characteristic_id = db.Column(db.BIGINT, db.ForeignKey('class_characteristic_op.id'))



