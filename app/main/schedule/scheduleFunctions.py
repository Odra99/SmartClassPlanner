from datetime import datetime, timedelta

def searchRestriction(restrictions,id):
    for restriction in restrictions:
        if(restriction.name==id.name):
            return restriction.value
        
    return None


def transformTimeDelta(time_str, format='%H:%M:%S'):
    time = datetime.strptime(
        str(time_str), format).time()
    return timedelta(
        hours=time.hour, minutes=time.minute)
