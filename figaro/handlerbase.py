"""handlers.py -- specific response handlers

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
from abc import abstractmethod
from .response import Response
from .memorykeys import MemoryKeys

class StatementHandlerBase(object):
    """Abstract base class for handling general statements."""

    @abstractmethod
    def can_handle(self, statement, memory):
        """Return true if this handler can respond to the statement"""
        pass

    @abstractmethod
    def handle(self, statement, memory):
        """Return a response to this statement"""
        pass

class DefaultStatementHandler(StatementHandlerBase):
    """Class to handle responses that other handlers can not respond to."""
    def can_handle(self, _, memory=None):
        return True

    def handle(self, statement, memory=None):
        topic = memory.get(MemoryKeys.key_topic())
        if not topic:
            return Response("I'm not sure how to respond to that.", [])
        else:
            return Response("Sorry. Are you still talking about the " \
                    + topic + "?", [])

class ConvoTerminationHandler(StatementHandlerBase):
    """Handle parting salutations such as 'bye'"""
    def can_handle(self, statement, memory):
        return self.handle(statement, memory) != None

    def handle(self, statement, memory):
        norm = statement.lower()
        if 'bye' in norm:
            return Response("See you later!", []).terminate_conversation()
        else:
            return None


if __name__ == '__main__':
    import doctest
    doctest.testmod()
