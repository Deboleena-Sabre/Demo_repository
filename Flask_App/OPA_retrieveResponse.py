


def Response_Block(responseBlock,len):
    start_pos = responseBlock.find("<Response>") + len
    end_pos = responseBlock.find("</Response>")
    FinalResponseBlock = responseBlock[start_pos:end_pos]
    return FinalResponseBlock