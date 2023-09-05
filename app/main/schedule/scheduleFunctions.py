def searchRestriction(restrictions,id):
    for i in range(len(restrictions)):
        if(restrictions.iloc[i]['name']==id):
            return restrictions.iloc[i]
        
    return None