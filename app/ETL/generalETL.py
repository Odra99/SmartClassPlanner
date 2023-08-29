import pandas as pd
from app.extensions import db
from app.model.general import Area


def etlArea(area):
    df = pd.read_csv(area)
    for i in range(len(df)):
        area = Area(name=df.iloc[i]['name'])
        db.session.add(area)
    db.session.commit()
    