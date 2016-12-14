"""greetingstatementhandler.py -- Greetings and salutations

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

from ..response import Response
from ..handlerbase import StatementHandlerBase

class GreetingStatementHandler(StatementHandlerBase):
    """For Greetings"""
    def can_handle(self, statement, memory=None):
        lowr = statement.lower()
        if 'hello' in lowr:
            return True
        if 'hey' in lowr and 'they' not in lowr:
            return True
        return False

    def handle(self, statement, memory=None):
        if 'hey' in statement.lower():
            return Response('Hey there.', [])
        return Response('Hello!', [])

if __name__ == '__main__':
    import doctest
    doctest.testmod()
