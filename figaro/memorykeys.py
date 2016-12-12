"""memorykeys.py -- static strings used by handlers

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

class MemoryKeys(object):
    """Specific locations in memory dictionary for certain information"""

    @staticmethod
    def key_interlocutor_name():
        """The key to the memory dict for the name of the user speaking to Figaro"""
        return '_interlocutor_name'

    @staticmethod
    def key_topic():
        """The key to the memory dict for the conversation topic"""
        return '_topic'

if __name__ == '__main__':
    import doctest
    doctest.testmod()
