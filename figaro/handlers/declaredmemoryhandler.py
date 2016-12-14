"""declaredmemoryhandler.py -- Reply with information from memory

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

class DeclaredMemoryHandler(StatementHandlerBase):
    """Handle statements that ask previously declared things"""
    def can_handle(self, statement, memory=None):
        return self.handle(statement, memory) != None

    def handle(self, statement, memory=None):
        """Handle a basic question

        >>> DeclaredMemoryHandler().handle('who is rodney?', {'rodney': 'a friend'}).answer
        'a friend'
        """
        norm = statement.lower()
        if " is " in norm:
            if "?" in norm or "wh" in norm:
                key_val = statement.split(" is ")
                key = key_val[1].replace('?', '')
                if memory.get(key):
                    return Response(str(memory[key]), [])
                else:
                    return None

        set_name = memory.get(MemoryKeys.key_interlocutor_name())
        if 'who am' in norm:
            if set_name:
                return Response("You told me your name is " + set_name + ".", [])
            else:
                return Response("I don't know. You tell me.", [])

        return None

if __name__ == '__main__':
    import doctest
    doctest.testmod()
