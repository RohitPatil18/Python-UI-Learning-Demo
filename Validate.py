

def validate(name) :
    if len(name)==0:
        return False

    j = 0
    for i in range(len(name)) :
        if name[i] == " " :
            if (i==j+1 or i==0) :
                return False
            else :
                j = i

    list = name.split()
    for i in list :
        if not i.isalpha() :
            return False

    return True
