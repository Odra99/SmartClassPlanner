from app.extensions import db, ma


class PriorityCriteria(db.Model):
    __tablename__ = "priority_criteria"
    id = db.Column(db.BIGINT, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    type = db.Column(db.BIGINT, db.ForeignKey('type.id'))
    subtype = db.Column(db.BIGINT, db.ForeignKey('type.id'))

class priorityCriteriaSchema(ma.Schema):
    class Meta:
        model=PriorityCriteria
        fields = ("id", "description")
    

priority_criteria_schema = priorityCriteriaSchema()
priority_criterias_schema = priorityCriteriaSchema(many=True)


class Type(db.Model):
    __tablename__ = "type"
    id = db.Column(db.BIGINT, primary_key=True)
    parent_type = db.Column(db.BIGINT, nullable=True)
    value = db.Column(db.String(250), nullable=False)


class Area(db.Model):
    __tablename__ = "area"
    id = db.Column(db.BIGINT, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(150), nullable=True)


class AreaSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "color")
    _links = ma.Hyperlinks(
        {
            "self": ma.URLFor("area_detail", values=dict(id="<id>")),
            "collection": ma.URLFor("areas"),
        }
    )

area_schema = AreaSchema()
areas_schema = AreaSchema(many=True)


class AreaOp(db.Model):
    __tablename__ = "area_oc"
    id = db.Column(db.BIGINT, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(150), nullable=True)
    schedule_id = db.Column(db.BIGINT,  db.ForeignKey('schedule.id'))

    schedule = db.relationship('Schedule', back_populates='areas')
    schedule_conf = db.relationship('ScheduleAreaConfiguration', back_populates='area')


class AreaOPSchema(ma.Schema):
    class Meta:
        model=AreaOp
        fields = ("id", "name", "color")
    

area_op_schema = AreaOPSchema()
areas_op_schema = AreaOPSchema(many=True)


class Restrictions(db.Model):
    __tablename__ = "restriction"
    id = db.Column(db.BIGINT, primary_key=True)
    type = db.Column(db.BIGINT, db.ForeignKey('type.id'))
    name = db.Column(db.String(150), nullable=False)
    value = db.Column(db.String(150), nullable=False)

class RestrictionsSchema(ma.Schema):
    class Meta:
        model=Restrictions
        fields = ("id", "name", "value")
    

restriction_schema = RestrictionsSchema()
restrictions_schema = RestrictionsSchema(many=True)

