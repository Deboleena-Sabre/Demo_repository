import pandas as pd

def createRemarkDataFrame(getReservationResponse):
    remarklineNo = ''
    lis = []
    start = getReservationResponse.find('Remarks>')
    start = start + 8
    end = getReservationResponse.find('</stl19:Remarks>')
    allRemarks = getReservationResponse[start:end]
    st = 0
    i = 1
    while(st!=-1):
        st = allRemarks.find('<stl19:Remark', st)
        if(st==-1):
            break
        else: 
            ed = allRemarks.find('</stl19:Remark>', st)
            ed = ed+16
            remark = allRemarks[st:ed]
            searchString = 'index="' + str(i) + '"'
            srt = remark.find(searchString)
            remarkLineNo = i
            in_pos = remark.find('<stl19:Text>')
            in_pos = in_pos +12
            nd = remark.find('</stl19:Text>')
            text = remark[in_pos:nd]
            lis.append([i,text])
            i = i+1
            st = ed
    df = pd.DataFrame(lis, columns =['Remark Line Number', 'RemarkText'])
    return df