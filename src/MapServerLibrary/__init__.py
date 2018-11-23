__version__ = '0.1'

from osgeo import ogr, osr, gdal
from robot.api.deco import keyword
import urllib.parse
import requests
from requests import Session, Request

class MapServerLibrary(object):

    """MapServerLibrary testing library for Robot Framework

    = Table of contents =

    - `Usage`
    - `Examples`

    = Usage =

    This library wraps mapserver calls. Contains keywords for the various ogc types.

    = Examples =

    | ${response}= | `MapServer.getfeatures` |
    | ${response}= | `MapServer.getfeaturecount` |
    | ${response}= | `MapServer.getlayers` |

    """

    def __init__(self, webservice_url = 'http://localhost', map_file = None, username = None, password = None):

        self._webservice_url = webservice_url
        resp = requests.get(self._webservice_url)
        self._map_file = map_file
        self._username=None
        self._password=None
        if resp.status_code == 401:
            self._username = username
            self._password = password

    @keyword('WFS.Get Feature Count')
    def get_feature_count(self, typename, sql_filter_key=None, sql_filter_value=None, version="1.1.0", srsname="EPSG:27700"):
        """Examples

        | ${result}= | MapServerLibrary.Get Feature Count | Secondary_Schools_OGC |
        | Should Be Equal As Integers | ${result} | 140 |
        
        """
        wfs_ds = self._get_ds(typename, sql_filter_key, sql_filter_value, version, srsname)
        layer = wfs_ds.GetLayerByName(typename)
        return layer.GetFeatureCount()
    
    def _get_ds(self, typename, sql_filter_key, sql_filter_value, version, srsname):
        if self._username:
            gdal.SetConfigOption('GDAL_HTTP_AUTH', 'NTLM')
            gdal.SetConfigOption('GDAL_HTTP_USERPWD',self._username + ':' + self._password)
        wfs_url = self._webservice_url + "VERSION=" + version + "&SRSNAME=" + srsname + "&SERVICE=WFS&REQUEST=GETFEATURE"
        if typename:
            wfs_url += "&TYPENAME=" + typename 
        wfs_url += "&MAP=" + self._map_file
        if sql_filter_key:
            wfs_url += "&" + sql_filter_key + "=" + urllib.parse.quote_plus(sql_filter_value)
        wfs_ds = ogr.Open('WFS:' + wfs_url)
        print(wfs_url)
        return wfs_ds
        
    @keyword('WFS.Get Features')
    def get_features(self, typename, sql_filter_key=None, sql_filter_value=None, version="1.1.0", srsname="EPSG:27700"):
        """Examples
        | ${result}= | MapServerLibrary.Get Features | Secondary_Schools_OGC |
        """
        features = []
        wfs_ds = self._get_ds(typename, sql_filter_key, sql_filter_value)
        layer = wfs_ds.GetLayerByName(typename)
        while True:
            feature = layer.GetNextFeature()
            if feature is None:
                break 
            features.append(feature)
        return features

    @keyword('WFS.Get Layers')
    def get_layers(self, version="1.1.0", srsname="EPSG:27700"):
        """Examples
        | ${result}= | MapServerLibrary.Get Layers | 
        """
        wfs_ds = self._get_ds(None, version, srsname)
        layers = []

        for i in range(wfs_ds.GetLayerCount()):
            layer = wfs_ds.GetLayerByIndex(i)
            layers.append(layer)

        return layers

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
        | ${result}= | MapServerLibrary.WMS.Get Map png | Parishes_OGC | 269800,32000,770200,278000 | 2502 | 1230 | 1.1.1 | EPSG:27700 | name=Parishes_OGC | nocache=1542205646127 | clientid=1542205605074_0921_20fc |
        """

        parameters = {
            'REQUEST': 'GetMap', 'FORMAT': 'image/png',
            'LAYERS': layers, 'VERSION': version,
            'SRS': srs, 'WIDTH' : width, 
            'HEIGHT': height, 'BBOX': bbox,
            'MAP': self._map_file
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
    
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'