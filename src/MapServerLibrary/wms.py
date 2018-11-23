from robot.api.deco import keyword
from requests import Request, Session
import requests

class WMSKeywords(object):

    def __init__(   self, 
                    webservice_url, 
                    map_file, 
                    username, 
                    password):
        self._webservice_url = webservice_url
        resp = requests.get(self._webservice_url)
        self._map_file = map_file
        self._username=None
        self._password=None
        if resp.status_code == 401:
            self._username = username
            self._password = password

    @keyword('WMS.Get Map png')
    def get_map_png(self, layers, 
                    bbox, width, height,
                    version="1.1.0", srs="EPSG:27700", 
                    mapsource='', styles='', 
                    transparent='', bgcolor='', 
                    exceptions='', time='', 
                    elevation='',sld='', 
                    wfs='', name='',
                    clientid='',nocache=''):
        
        """ Makes a getmap request to return a response object containing details about the image retrieved

        Examples:
        | ${result}= | MapServerLibrary.WMS.Get Map png | Parishes_OGC | 269800,32000,770200,278000 | 2502 | 1230 | 1.1.1 | EPSG:27700 | name=Parishes_OGC | sld=sld-C1542205605074_0921_20fc.xml | nocache=1542205646127 | clientid=1542205605074_0921_20fc |
        """

        parameters = {
            'REQUEST': 'GetMap', 'FORMAT': 'image/png',
            'LAYERS': layers, 'VERSION': version,
            'SRS': srs, 'WIDTH' : width, 
            'HEIGHT': height, 'BBOX': bbox,
            'MAP:': self._map_file
        }

        optional_params = [
                'mapsource', 'styles', 'transparent', 'bgcolor', 'exceptions',
                'time', 'elevation', 'sld', 'wfs', 'name', 'clientid', 'nocache'
        ]

        for param in optional_params:
                param_value = vars()[param]
                if param_value != '':
                    parameters[param.upper()] = param_value

        session = Session()
        if self._username is not None and self._password is not None:
            session.auth = HttpNtlmAuth(self._username, self._password)
        req = Request('GET', self._webservice_url, params=parameters)
        prepped = session.prepare_request(req)
        resp = session.send(prepped)
    
        return resp
        