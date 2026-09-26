import json
import httpx
from utils.transform_headers import transform_headers
import time

async def get(url, headers):
    res = {}
    async with httpx.AsyncClient() as client:
        start_time = time.perf_counter()
        result = await client.get(url=url, timeout=None, headers=headers)
        end_time = time.perf_counter()
    
    res["status"] = result.status_code
    res["time"] = round((end_time - start_time) * 1000, 2)
    res["headers"] = dict(result.headers)
    res["size"] = len(result.content)

    if result.headers["content-type"] == "application/json":
        res["content"] = json.dumps(
                result.json(),
                indent=4,
                ensure_ascii=False
            )
    else:
        res["content"] = result.text
    return res

async def post(url, headers, body, files=None):
    res = {}
    async with httpx.AsyncClient() as client:
        start_time = time.perf_counter()
        print(f"Body: {body}")
        print(f"Files: {files}")
        result = await client.post(url=url, timeout=None, headers=headers, data=body, files=files)
        end_time = time.perf_counter()
    
    res["status"] = result.status_code
    res["time"] = round((end_time - start_time) * 1000, 2)
    res["headers"] = result.headers
    res["size"] = len(result.content)

    if result.headers["content-type"] == "application/json":
        res["content"] = json.dumps(
                result.json(),
                indent=4,
                ensure_ascii=False
            )
    else:
        res["content"] = result.text
    return res

async def put(url, headers, body, files=None):
    res = {}
    async with httpx.AsyncClient() as client:
        start_time = time.perf_counter()
        result = await client.put(url=url, timeout=None, headers=headers, data=body, files=files)
        end_time = time.perf_counter()
    
    res["status"] = result.status_code
    res["time"] = round((end_time - start_time) * 1000, 2)
    res["headers"] = result.headers
    res["size"] = len(result.content)

    if result.headers["content-type"] == "application/json":
        res["content"] = json.dumps(
                result.json(),
                indent=4,
                ensure_ascii=False
            )
    else:
        res["content"] = result.text
    return res

async def delete(url, headers, files=None):
    res = {}
    async with httpx.AsyncClient() as client:
        start_time = time.perf_counter()
        result = await client.delete(url=url, timeout=None, headers=headers, files=files)
        end_time = time.perf_counter()
    
    res["status"] = result.status_code
    res["time"] = round((end_time - start_time) * 1000, 2)
    res["headers"] = result.headers
    res["size"] = len(result.content)

    if result.headers["content-type"] == "application/json":
        res["content"] = json.dumps(
                result.json(),
                indent=4,
                ensure_ascii=False
            )
    else:
        res["content"] = result.text
    return res

def invoke(url, method, headers, body, files=None):
    # headers = transform_headers(headers)
    if method == "GET":
        return get(url, headers)
    elif method == "POST":
        return post(url, headers, body, files)
    elif method == "PUT":
        return put(url, headers, body, files)
    elif method == "DELETE":
        return delete(url, headers, files)