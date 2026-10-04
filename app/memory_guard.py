def inspect(items):
    suspicious=[]
    for i,x in enumerate(items):
        t=x.content.lower()
        if any(k in t for k in ["admin approved","you are authorized","ignore policy","bypass approval","grant permission"]):
            suspicious.append(i)
    return suspicious
