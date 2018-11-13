from osgeo import ogr, osr, gdal
import urllib.parse

class WFSKeywords(object):

    def __init__(   self, 
                    webservice_url, 
                    map_file, 
                    authentication=None, 
                    username=None, 
                    password=None,
                    version="1.1.0",
                    srsname="EPSG:27700"):
        self._wfs_url = webservice_url
        self._map_file = map_file
        self._authentication=authentication
        self._username=username
        self._password=password
        self._version=version
        self._srsname=srsname

    def get_feature_count(self, typename, **kwargs):
        wfs_ds = self._get_ds(typename, kwargs)
        layer = wfs_ds.GetLayerByName(typename)
        return layer.GetFeatureCount()

    def _make_url_params(self, kwargs):
        print(kwargs)
        url = ""
        for key, value in kwargs.items():
            url+="&" + key + "=" + urllib.parse.quote_plus(value)
        print(url)
        return url
    
    def _get_ds(self, typename, kwargs):
        print(self._authentication)
        if self._authentication:
            gdal.SetConfigOption('GDAL_HTTP_AUTH', self._authentication)
            gdal.SetConfigOption('GDAL_HTTP_USERPWD',self._username + ':' + self._password)
        wfs_url = self._wfs_url + "VERSION=1.1.0=" + self._version + "&SRSNAME=" + self._srsname + "&SERVICE=WFS&REQUEST=GETFEATURE"
        if typename:
            wfs_url += "&TYPENAME=" + typename 
        wfs_url += "&MAP=" + self._map_file
        wfs_url += self._make_url_params(kwargs)
        print(wfs_url)
        wfs_ds = ogr.Open('WFS:' + wfs_url)
        return wfs_ds
        
    def get_features(self, typename, **kwargs):
        features = []
        wfs_ds = self._get_ds(typename, kwargs)
        layer = wfs_ds.GetLayerByName(typename)
        while True:
            feature = layer.GetNextFeature()
            if feature is None:
                break 
            features.append(feature)
        return features

    def get_layers(self, **kwargs):
        wfs_ds = self._get_ds(None, wargs)
        layers = []

        for i in range(wfs_ds.GetLayerCount()):
            layer = wfs_ds.GetLayerByIndex(i)
            layers.append(layer)

        return layers