from MapServerLibrary.wfs import WFSKeywords
from MapServerLibrary.wms import WMSKeywords

__version__ = '0.1'

class MapServerLibrary(WMSKeywords, WFSKeywords):

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

    def __init__(self, webservice_url = 'http://localhost', mapfile = None, username = None, password = None):

        super().__init__(webservice_url, mapfile, username, password)
        #WFS = WFSKeywords(webservice_url, mapfile, username, password)
        #WMS = WMSKeywords(webservice_url, mapfile, username, password)
        #WFS = WFSKeywords(webservice_url, mapfile, username, password)
        #WMS = WMSKeywords(webservice_url, mapfile, username, password)
    
        ROBOT_LIBRARY_SCOPE = 'GLOBAL'