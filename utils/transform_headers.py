def transform_headers(headers:str):
    headers_dict = {}
    lines = headers.split("\n")
    # print(lines)
    for line in lines:
        if len(line) != 0:
            k, v = line.split(": ")
            headers_dict[k] = v

    return headers_dict