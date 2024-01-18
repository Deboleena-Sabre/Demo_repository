

def SignInDetails():
    file = open("/Users/ShubhamKhandelwal/Documents/OPA_Robot_working/SignInDetails.txt","r")
    content = file.readlines()
    dict = {}
    for i in content:
        ind = i.find(':')
        ind1 = i.find('\n')
        credName = i[:ind]
        credValue = i[ind+1:ind1]
        credValue.strip()
        dict[str(credName)] = str(credValue)

    return dict

