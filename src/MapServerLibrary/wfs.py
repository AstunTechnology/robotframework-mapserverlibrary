from osgeo import ogr, osr, gdal
from robot.api.deco import keyword
import urllib.parse
import requests

class WFSKeywords(object):

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