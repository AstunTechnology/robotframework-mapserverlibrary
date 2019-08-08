from requests import Session, Request
from robot.api import logger

def make_request(method, url, parameters={}, data={}, headers={}, username=None, password=None):
    session = Session()
    if username is not None and password is not None:
        session.auth = HttpNtlmAuth(username, password)

    logger.debug("URL: {0}".format(url))
    logger.debug("Parameters: {0}".format(parameters))
    logger.debug("Headers: {0}".format(headers))
    logger.debug("Data: {0}".format(data))

    req = Request(method, url, params=parameters, data=data, headers=headers)
    prepped = session.prepare_request(req)
    resp = session.send(prepped)


    content_type = resp.headers.get('content-type')
    logger.debug("Content-Type: {0}".format(content_type))
    if "text" in content_type:
        logger.debug("Response:\r\n{0}".format(resp.text))

    return resp