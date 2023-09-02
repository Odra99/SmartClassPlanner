from app.extensions import db
from app.model.general import Area
from app.ETL.generalFunctions import getDataFrame


def etlArea(url):
    df = getDataFrame(url)
    for i in range(len(df)):
        aux = Area(name=df.iloc[i]['name'])
        db.session.add(aux)
    db.session.commit()
    