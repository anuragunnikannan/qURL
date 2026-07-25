def transform_headers(headers:str):
    headers_dict = {}
    lines = headers.split("\n")
    # print(lines)
    for line in lines:
        if len(line) != 0:
            k, v = line.split(": ")
            headers_dict[k] = v

    return headers_dict

def transform_headers_dict(headers_dict:dict):
    headers = ""
    for k, v in headers_dict.items():
        headers += f"{k}: {v}\n"
    
    return headers