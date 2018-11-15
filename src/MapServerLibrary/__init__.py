
from MapServerLibrary.wfs import WFSKeywords

__version__ = '0.1'

class MapServerLibrary(WFSKeywords):

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
    
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'