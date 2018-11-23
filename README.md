``MapServerLibrary`` is a [Robot Framework](http://code.google.com/p/robotframework/) test library to abstract test calls to [mapserver](https://mapserver.org) (v6.4) 

# Usage

```
Install python3
pip install robotframework
python setup.py install
```

Sample test case

```
| *** Test Cases *** |
| Test basic WFS Request |
|                   | ${result}= | MapServerLibrary.WFS.Get Feature Count | Secondary_Schools_OGC |
|                   | Should Be Equal As Integers | ${result} | 140 |
```


view MapServerLibrary.html in a browser to view full keyword documentation.

# Help

Send your questions to the [Robot Framework Users Group](https://groups.google.com/forum/#!forum/robotframework-users)
