"""figaro.py

   Copyright 2016 Rylan Santinon

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

class Figaro(object):
    """Figaro -- the personal assistant"""
    def __init__(self):
        pass

    def greet(self):
        """Greet the user

        >>> Figaro().greet()
        'Call me Figaro.'
        """
        return "Call me Figaro."

if __name__ == '__main__':
    import doctest
    doctest.testmod()
