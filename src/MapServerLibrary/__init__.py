__version__ = '0.1'

from osgeo import ogr, osr, gdal
from robot.api import logger
from robot.api.deco import keyword
import urllib.parse
import requests
import re
from MapServerLibrary.HTTPRequest import make_request


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

    def __init__(self, mapserver_url = 'http://localhost', map_file = None, username = None, password = None):

        self._mapserver_url = mapserver_url
        resp = requests.get(self._mapserver_url)
        self._map_file = map_file
        self._username=None
        self._password=None
        if resp.status_code == 401:
            self._username = username
            self._password = password

    def _get_ds(self, typename, sql_filter_key, sql_filter_value, version, srsname):
        if self._username:
            gdal.SetConfigOption('GDAL_HTTP_AUTH', 'NTLM')
            gdal.SetConfigOption('GDAL_HTTP_USERPWD',self._username + ':' + self._password)
        wfs_url = self._mapserver_url + "VERSION=" + version + "&SRSNAME=" + srsname + "&SERVICE=WFS&REQUEST=GETFEATURE"
        if typename:
            wfs_url += "&TYPENAME=" + typename
        wfs_url += "&MAP=" + self._map_file
        if sql_filter_key:
            wfs_url += "&" + sql_filter_key + "=" + urllib.parse.quote_plus(sql_filter_value)
        wfs_ds = ogr.Open('WFS:' + wfs_url)
        print(wfs_url)
        return wfs_ds

    def get_file_contents(self, url):
        r = requests.get(url, stream=True)
        return r.content

    @keyword('Is Mapserver Installed')
    def is_mapserver_installed(self):
        """Makes an empty request to mapserver to ensure
        it is installed and configured correctly

        Example:
        | | ${installed}= | MapServerLibrary.Is Mapserver Installed |
        | | Should Be True | ${installed} |"""

        req = make_request('GET', self._mapserver_url, username=self._username, password=self._password)
        if req.status_code != 200:
            return False

        text = req.text
        if not "No query information to decode. QUERY_STRING is set, but empty." in text:
            return False

        return True

    @keyword('Get Mapserver Version')
    def get_mapserver_version(self):
        """Makes a request to mapserver to retrieve
        the version number

        Example:
        | | ${version}= | MapServerLibrary.Get Mapserver Version |
        | | Should Be Equal As Strings | ${result.major} | ${7} |
        | | Should Be Equal As Strings | ${result.minor} | ${4} |
        | | Should Be Equal As Strings | ${result.point} | ${0} |
        """
        emptyVersionDict = { "major": "0", "minor": "0", "point": "0" }

        resp = make_request("GET", "{0}?map=".format(self._mapserver_url), username=self._username, password=self._password)
        version = re.search(r"MapServer version (\d{1,}\.\d{1,}\.\d{1,})", resp.text, re.IGNORECASE)[1]
        if version is None:
            return emptyVersionDict

        versionSplit = version.split(".")
        if len(versionSplit) != 3:
            return emptyVersionDict

        return { "major": versionSplit[0], "minor": versionSplit[1], "point": versionSplit[2] }

    @keyword('Browse')
    def browse(self, mapfile="", x=None, y=None, layers=""):
        pass

    @keyword('Query')
    def query(self, mapfile="", x=None, y=None, layers="", tolerance=0.1, template=""):
            """Makes a mapserver query request"""

            parameters = {
                "mode": "query",
                "map": mapfile,
                "layers": layers,
            }

            for layer in layers.split(','):
                parameters["map.layer[{0}]".format(layer)] = "TOLERANCE {0} TEMPLATE '{1}' TOLERANCEUNITS METERS".format(tolerance, template)

            if x is not None and y is not None:
                parameters["mapxy"] = "{0} {1}".format(str(x), str(y))

            resp = make_request("GET", self._mapserver_url, parameters=parameters, username=self._username, password=self._password)

            return resp.text

    @keyword('Nquery')
    def nquery(self, mapfile="", x=None, y=None, mapshape="", layers="", tolerance=0.1, template=""):
            """Makes a mapserver NQuery request"""

            parameters = {
                "mode": "nquery",
                "map": mapfile,
                "layers": layers,
            }

            for layer in layers.split(','):
                parameters["map.layer[{0}]".format(layer)] = "TOLERANCE {0} TEMPLATE '{1}' TOLERANCEUNITS METERS".format(tolerance, template)

            if x is not None and y is not None:
                parameters["mapxy"] = "{0} {1}".format(str(x), str(y))
            elif mapshape != '':
                parameters["mapshape"] = mapshape

            resp = make_request("GET", self._mapserver_url, parameters=parameters, username=self._username, password=self._password)

            return resp.text

    @keyword('Itemquery')
    def itemquery(self, mapfile="", query="", field="", layer="", tolerance=0.1, template=""):
            """Makes a mapserver ItemQuery request"""

            parameters = {
                "mode": "itemquery",
                "map": mapfile,
                "qlayer": layer,
            }

            parameters["map.layer[{0}]".format(layer)] = "TOLERANCE {0} TEMPLATE '{1}' TOLERANCEUNITS METERS".format(tolerance, template)

            if query is not None and field is not None:
                parameters["qstring"] = "{0}='{1}'".format(field, query)

            resp = make_request("GET", self._mapserver_url, parameters=parameters, username=self._username, password=self._password)

            return resp.text

    # @keyword('Itemnquery')
    # def itemnquery(self, mapfile="", query="", layers="", tolerance=0.1, template=""):
    #         """Makes a mapserver ItemNQuery request"""

    #         parameters = {
    #             "mode": "itemnquery",
    #             "map": mapfile,
    #             "layers": layers,
    #         }

    #         for layer in layers.split(','):
    #             parameters["map.layer[{0}]".format(layer)] = "TOLERANCE {0} TEMPLATE '{1}' TOLERANCEUNITS METERS".format(tolerance, template)

    #         if query is not None:
    #             parameters["query"] = query

    #         resp = make_request("GET", self._mapserver_url, parameters=parameters, username=self._username, password=self._password)

    #         return resp.text

    # @keyword('Featurequery')
    # def itemquery(self, mapfile="", query="", layers="", tolerance=0.1, template=""):
    #         """Makes a mapserver FeatureQuery request"""

    #         parameters = {
    #             "mode": "featurequery",
    #             "map": mapfile,
    #             "layers": layers,
    #         }

    #         for layer in layers.split(','):
    #             parameters["map.layer[{0}]".format(layer)] = "TOLERANCE {0} TEMPLATE '{1}' TOLERANCEUNITS METERS".format(tolerance, template)

    #         if query is not None:
    #             parameters["query"] = query

    #         resp = make_request("GET", self._mapserver_url, parameters=parameters, username=self._username, password=self._password)

    #         return resp.text

    # @keyword('Featurenquery')
    # def itemnquery(self, mapfile="", query="", layers="", tolerance=0.1, template=""):
    #         """Makes a mapserver FeatureNQuery request"""

    #         parameters = {
    #             "mode": "featurenquery",
    #             "map": mapfile,
    #             "layers": layers,
    #         }

    #         for layer in layers.split(','):
    #             parameters["map.layer[{0}]".format(layer)] = "TOLERANCE {0} TEMPLATE '{1}' TOLERANCEUNITS METERS".format(tolerance, template)

    #         if query is not None:
    #             parameters["query"] = query

    #         resp = make_request("GET", self._mapserver_url, parameters=parameters, username=self._username, password=self._password)

    #         return resp.text

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
                    clientid='',nocache='',
                    **kwargs):

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

        #Add any kwargs for template params
        for key, value in kwargs.items():
            parameters[key] = value

        resp = make_request('GET', self._mapserver_url, parameters=parameters, data={}, headers={}, username=self._username, password=self._password)

        return resp

    @keyword('WMS.Get Legend Graphic png')
    def get_legend_graphic( self, layer, format, sld_url, version='1.1.0', srs='EPSG:27700'):
        """Examples

        | ${result}= | MapServerLibrary.Get Legend Graphic png | Secondary_Schools_OGC | image/png |

        """

        return self._mapserver_post(
                                     service='WMS', request= 'GetLegendGraphic', format='image/png', sld_url = sld_url,
                                     version=version, srs=srs, layer=layer
                                     )

    @keyword('WFS.Get Feature Count')
    def get_feature_count(self, typename, sql_filter_key=None, sql_filter_value=None, version="1.1.0", srsname="EPSG:27700"):
        """Examples

        | ${result}= | MapServerLibrary.Get Feature Count | Secondary_Schools_OGC |
        | Should Be Equal As Integers | ${result} | 140 |

        """
        wfs_ds = self._get_ds(typename, sql_filter_key, sql_filter_value, version, srsname)
        layer = wfs_ds.GetLayerByName(typename)
        return layer.GetFeatureCount()

    @keyword('WMS.Get Map png Post')
    def get_map_png_post(   self, layers,
                            bbox, width, height,
                            version='1.1.0', srs='EPSG:27700',
                            mapsource='',
                            styles='', transparent='',
                            bgcolor='', exceptions='',
                            time='', elevation='',
                            sld_url='', sld_body='',
                            wfs='', name='',
                            clientid='',nocache='',
                            **kwargs):

        return self._mapserver_post( layers=layers, bbox=bbox,
                                     width=width, height=height,
                                     service='WMS', request= 'GetMap', format='image/png',
                                     version=version, srs=srs,
                                     mapsource=mapsource,
                                     styles=styles, transparent=transparent,
                                     bgcolor=bgcolor, exceptions=exceptions,
                                     time=time, elevation=elevation,
                                     sld_url=sld_url, sld_body=sld_body,
                                     wfs=wfs, name=name,
                                     clientid=clientid, nocache=nocache,
                                     **kwargs)

    def _mapserver_post(  self,
                          service, request, format,
                          version='1.1.0', srs='EPSG:27700',
                          layers='', bbox='', width='', height='',
                          mapsource='',
                          styles='', transparent='',
                          bgcolor='', exceptions='',
                          time='', elevation='',
                          sld_url='', sld_body='',
                          wfs='', name='',
                          clientid='',nocache='',
                          **kwargs):

        """ Makes a getmap request to a given URL which may contain mapserver parameters. Remaining parameters can be
            sent via a POST request. If a URL is passed through the sld_url parameter, then the sld file contents
            will be pulled from there and passed into sld_body.
        """

        parameters = {
                    'REQUEST': request, 'FORMAT': format, 'SERVICE': service,
                    'VERSION': version,
                    'SRS': srs }

        optional_params = [
                    'mapsource', 'styles', 'transparent', 'bgcolor', 'exceptions',
                    'time', 'elevation', 'sld_body', 'sld_url', 'wfs', 'name', 'clientid', 'nocache',
                    'layers', 'width', 'height', 'bbox'
        ]

        for param in optional_params:
            param_value = vars()[param]
            if param_value != '':
                parameters[param.upper()] = param_value

        if 'SLD_URL' in parameters:
            parameters['SLD_BODY'] = self.get_file_contents(parameters['SLD_URL'])
            del parameters['SLD_URL']

        #Add any kwargs for template params
        for key, value in kwargs.items():
            parameters[key] = value

        req = make_request('POST', self._mapserver_url, parameters={}, data=parameters, headers={}, username=self._username, password=self._password)

        return req

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'