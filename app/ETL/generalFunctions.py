import pandas as pd
from app.extensions import db
from sqlalchemy import text

def getDataFrame(url):
    return pd.read_csv(url)

def searchAreaByName(areas,name):
    for area in areas:
        if(area.name==name):
            return area
    return None

def truncateTable(table_name):
    engine = db.engine
    truncate_query = text(f'''  TRUNCATE TABLE {table_name} CASCADE; ''')

    with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as connection:
        connection.execute(truncate_query)