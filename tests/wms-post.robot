*** Settings ***

Documentation       Test WMS responses

| *Setting*         | *Value*           |
| Library			| MapServerLibrary  | http://52.212.160.2/mapserver/ms64?map=E:\\iShareData\\LIVE\\_MapServerConfig\\mapsources__AllMaps.map&user=jon@win-3a4t9adpotv&Total_Street_Crimes_sql=(SELECT sum("total_crime") AS "total_crime", "ogc_fid" FROM ( SELECT * FROM "public"."police_streetcrime_crosstab" ) q GROUP BY "ogc_fid") | E:\\iShareData\\LIVE\\_MapServerConfig\\mapsources__AllMaps.map |

| *Variables*       |
| ${BBOX}           | 316996.5,126671.25,355771.5,160758.75 |
| ${HEIGHT}         | 1551 |
| ${WIDTH}          | 1363 |
| ${MAPSOURCE}      | jon@WIN-3A4T9ADPOTV:mapsources/AllMaps |
| ${SLD_URL}        | http://52.212.160.2/isharegislive.webservice/sld/sld-S8ec97f65-23ca-449c-abcb-6f02eba857f7.xml |

| *** Test Cases *** |

| GetImage Response status |
|                   | ${result}= | MapServerLibrary.WMS.Get Map png POST | Total_Street_Crimes | ${BBOX} | ${HEIGHT} | ${WIDTH} | 1.1.1 | EPSG:27700 | mapsource=${MAPSOURCE} | nocache=1543337076475 | sld_url=${SLD_URL} | name=Total_Street_Crimes | clientid=1543336397369_0574_1b3f |
|                   | Should Be Equal As Integers | ${result.status_code} | 200 |
|                   | Log | ${result.content} |

| GetImage Content Type    |
|                   | ${result}= | MapServerLibrary.WMS.Get Map png POST | Total_Street_Crimes | ${BBOX} | ${HEIGHT} | ${WIDTH} | 1.1.1 | EPSG:27700 | mapsource=${MAPSOURCE} | nocache=1543337076475 | sld_url=${SLD_URL} | name=Total_Street_Crimes | clientid=1543336397369_0574_1b3f |
|                   | Should Be Equal As Strings | ${result.headers.get('content-type')} | image/png |

| GetImage Size            |
|                   | ${result}= | MapServerLibrary.WMS.Get Map png POST | Total_Street_Crimes | ${BBOX} | ${HEIGHT} | ${WIDTH} | 1.1.1 | EPSG:27700 | mapsource=${MAPSOURCE} | nocache=1543337076475 | sld_url=${SLD_URL} | name=Total_Street_Crimes | clientid=1543336397369_0574_1b3f |
|                   | Should Be True | ${result.headers.get('content-length')} >= 82000 |
|                   | Should Be True | ${result.headers.get('content-length')} <= 83000 |