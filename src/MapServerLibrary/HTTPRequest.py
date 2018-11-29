from requests import Session, Request

def make_request(method, url, parameters={}, data={}, headers={}, username=None, password=None):
    session = Session()
    if self._username is not None and self._password is not None:
        session.auth = HttpNtlmAuth(self._username, self._password)
    req = Request(method, url, params=parameters, data=data, headers=headers)
    prepped = session.prepare_request(req)
    resp = session.send(prepped)
    return resp