#!/usr/bin/env python

#  Copyright (c) 2010 Franz Allan Valencia See
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.


"""Setup script for Robot's MapServer distributions"""

from setuptools import setup

__version__ = '0.1.7'

def main():
    setup(name         = 'robotframework-mapserverlibrary',
          version      = __version__,
          description  = 'MapServer utility library for Robot Framework',
          author       = 'Jonathan Lake-Thomas',
          author_email = 'jonathanlakethomas@astuntechnology.com',
          url          = 'https://github.com/AstunTechnology/robotframework-mapserverlibrary',
          package_dir  = { '' : 'src'},
          packages     = ['MapServerLibrary'],
          install_requires = ['GDAL>=2.3.2','requests>=2.2.0','requests_ntlm>=1.1.0', 'urllib3']
          )
        

if __name__ == "__main__":
    main()