from requests import Session, Request

def make_request(method, url, parameters={}, data={}, headers={}, username=None, password=None):
    session = Session()
    if username is not None and password is not None:
        session.auth = HttpNtlmAuth(username, password)
    req = Request(method, url, params=parameters, data=data, headers=headers)
    prepped = session.prepare_request(req)
    resp = session.send(prepped)
    return resp