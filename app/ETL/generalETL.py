from app.extensions import db
from app.model.general import Area
from app.ETL.generalFunctions import getDataFrame,truncateTable


def etlArea(url):
    truncateTable('area')
    df = getDataFrame(url)
    areas = []
    for i in range(len(df)):
        aux = Area(name=df.iloc[i]['name'])
        
        db.session.add(aux)
        areas.append(aux)
    db.session.commit()
    return areas


