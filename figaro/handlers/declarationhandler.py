"""delcarationhandler.py -- Memorizing statements and equalities

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
from ..memorykeys import MemoryKeys
from ..handlerbase import StatementHandlerBase

class DeclarationHandler(StatementHandlerBase):
    """Handle declarative statements"""
    def can_handle(self, statement, memory=None):
        return self.handle(statement, memory) != None

    def handle(self, statement, memory=None):
        norm = statement.lower()
        if " is " not in norm:
            return None
        if "?" in norm:
            return None

        key_val = statement.split(" is ")
        key = key_val[0].lower()
        val = key_val[1]

        ans = "Thanks for letting me know."
        to_mem = [(key, val)]

        if "my name is" in norm:
            ans = "Nice to meet you."
            to_mem.append((MemoryKeys.key_interlocutor_name(), val))

        return Response(ans, to_mem)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
