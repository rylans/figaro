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
from abc import abstractmethod

class StatementHandlerBase(object):
    """Abstract base class for handling general statements."""

    @abstractmethod
    def can_handle(self, statement):
        """Return true if this handler can respond to the statement"""
        pass

    @abstractmethod
    def handle(self, statement):
        """Return a response to this statement"""
        pass

class DefaultStatementHandler(StatementHandlerBase):
    """Class to handle responses that other handlers can not respond to."""
    def can_handle(self, _):
        return True

    def handle(self, _):
        return Response("I'm not sure how to respond to that.", [])

class GreetingStatementHandler(StatementHandlerBase):
    """For Greetings"""
    def can_handle(self, statement):
        lowr = statement.lower()
        if 'hello' in lowr:
            return True
        if 'hey' in lowr:
            return True
        return False

    def handle(self, statement):
        if 'hey' in statement.lower():
            return Response('Hey there.', [])
        return Response('Hello!', [])

class Response(object):
    """Response to a question or statement

    >>> Response('Certainly.', []).answer
    'Certainly.'

    >>> Response('I will.', [])
    <Response 'I will.'>
    """
    def __init__(self, answer, memo):
        self._answer = answer
        self._memo = memo

    @property
    def answer(self):
        return self._answer

    def __repr__(self):
        return "<Response '%s'>" % self.answer

class Figaro(object):
    """Figaro -- the personal assistant"""
    def __init__(self):
        self._handlers = []
        self._handlers.append(GreetingStatementHandler())
        self._handlers.append(DefaultStatementHandler())

    def _dispatch_to_handler(self, statement):
        for handler in self._handlers:
            if handler.can_handle(statement):
                return handler.handle(statement)
        raise RuntimeError('No handler registered for statement "%s"' % statement)

    def hears(self, statement):
        """Accept the given statement and respond to it

        >>> Figaro().hears("Hello there")
        'Hello!'

        >>> Figaro().hears("jibberjabber")
        "I'm not sure how to respond to that."
        """
        return self._dispatch_to_handler(statement).answer

if __name__ == '__main__':
    import doctest
    doctest.testmod()
