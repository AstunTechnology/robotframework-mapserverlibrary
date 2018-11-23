*** Settings ***

Documentation       Test WMS responses

| *Setting*         | *Value*           |
| Library			| MapServerLibrary  | http://52.212.160.2/mapserver/ms64? | E:\\iShareData\\LIVE\\_MapServerConfig\\mapsources__AllMaps.map |

| *** Test Cases *** |

| GetImage Response status |
|                   | ${result}= | MapServerLibrary.WMS.Get Map png | New_OGC_Layer | 316996.5,126671.25,355771.5,160758.75 | 1551 | 1363 | 1.1.1 | EPSG:27700 | name=New_OGC_Layer | nocache=1542205646127 | clientid=1542205605074_0921_20fc |
|                   | Should Be Equal As Integers | ${result.status_code} | 200 |

| GetImage Content Type    |
|                   | ${result}= | MapServerLibrary.WMS.Get Map png | New_OGC_Layer | 316996.5,126671.25,355771.5,160758.75 | 1551 | 1363 | 1.1.1 | EPSG:27700 | name=New_OGC_Layer | nocache=1542205646127 | clientid=1542205605074_0921_20fc |
|                   | Should Be Equal As Strings | ${result.headers.get('content-type')} | image/png |

| GetImage Size            |
|                   | ${result}= | MapServerLibrary.WMS.Get Map png | New_OGC_Layer | 316996.5,126671.25,355771.5,160758.75 | 1551 | 1363 | 1.1.1 | EPSG:27700 | name=New_OGC_Layer | nocache=1542205646127 | clientid=1542205605074_0921_20fc |
|                   | Should Be True | ${result.headers.get('content-length')} >= 30000 |
|                   | Should Be True | ${result.headers.get('content-length')} <= 40000 |