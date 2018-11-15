*** Settings ***
Documentation     WFS Based Tests using keyword-driven testing approach.
...
| *Setting*          | *Value*           |
| Library            | MapServerLibrary  | http://127.0.0.1/mapserver/ms64?  | D:\\iShareData\\Astun\\_MapServerConfig\\astun__default.map |

| *** Variables ***  |
| ${TestSQL}         | (SELECT * FROM (SELECT * FROM (SELECT * FROM "education"."secondary_schools") viewparams_inner) viewparams_outer WHERE gender_name = 'Girls') |

| *** Test Cases *** |
| Test basic WFS Request |
|                   | ${result}= | MapServerLibrary.Get Feature Count | Secondary_Schools_OGC |
|                   | Should Be Equal As Integers | ${result} | 140 |

| Test WFS with SQL Filter |
|                   | ${result}= | MapServerLibrary.Get Feature Count | Secondary_Schools_OGC | Secondary_Schools_OGC_sql=${TestSQL} | x=y |
|                   | Should Be Equal As Integers | ${result} | 12 |