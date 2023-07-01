def respond_with(message: str, status=200, data: list | dict | None = None):
    res = {"status": status, "message": message}

    if data:
        res["data"] = data
        return res

    return res
