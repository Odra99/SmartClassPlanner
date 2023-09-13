from datetime import datetime, timedelta

def searchRestriction(restrictions,id):
    for i in range(len(restrictions)):
        if(restrictions.iloc[i]['name']==id):
            return restrictions.iloc[i]
        
    return None


def transformTimeDelta(time_str, format='%H:%M:%S'):
    time = datetime.strptime(
        str(time_str), format).time()
    return timedelta(
        hours=time.hour, minutes=time.minute)
