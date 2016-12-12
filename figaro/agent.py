"""agent.py -- personal assistant and modular chat bot

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
from copy import deepcopy

from .handlers import (GreetingStatementHandler,
                       ArithmeticHandler,
                       DeclaredMemoryHandler,
                       DeclarationHandler,
                       ConvoTerminationHandler,
                       ElizaStatementHandler,
                       DefaultStatementHandler)

class Figaro(object):
    """Figaro -- the personal assistant"""
    def __init__(self):
        self._conv_ended = False
        self._memory = {}
        self._handlers = []
        self._handlers.append(GreetingStatementHandler())
        self._handlers.append(ArithmeticHandler())
        self._handlers.append(DeclaredMemoryHandler())
        self._handlers.append(DeclarationHandler())
        self._handlers.append(ConvoTerminationHandler())
        self._handlers.append(ElizaStatementHandler())
        self._handlers.append(DefaultStatementHandler())

    @property
    def conversation_ended(self):
        return self._conv_ended

    def _mem_store(self, key, val):
        self._memory[key] = val

    def _dispatch_to_handler(self, statement):
        for handler in self._handlers:
            copied_mem = deepcopy(self._memory)
            if handler.can_handle(statement, copied_mem):
                return handler.handle(statement, copied_mem)
        raise RuntimeError('No handler registered for statement "%s"' % statement)

    def hears(self, statement):
        """Accept the given statement and respond to it

        >>> Figaro().hears("Hello there")
        'Hello!'

        >>> Figaro().hears("5 minus 13")
        '-8.0'

        >>> Figaro().hears("jibberjabber")
        "I'm not sure how to respond to that."

        >>> Figaro().hears("Why are you so rude?")
        'I was born that way.'

        >>> Figaro().hears("Are you deaf?")
        'Yes. How about you?'

        >>> Figaro().hears("you are really annoying")
        'In what way exactly?'

        >>> fg = Figaro()
        >>> fg.hears("who am i")
        "I don't know. You tell me."
        >>> fg.hears("alabama is in America.")
        'Thanks for letting me know.'
        >>> fg.hears("Where is alabama?")
        'in America.'
        >>> fg.hears("My name is Ishmael")
        'Nice to meet you.'
        >>> fg.hears("What is my name?")
        'Ishmael'
        >>> fg.hears("who am I?")
        'You told me your name is Ishmael.'
        """
        response = self._dispatch_to_handler(statement)

        if response.terminated:
            self._conv_ended = True

        answer, memos = response.answer, response.memo

        for memo in memos:
            key, val = memo
            self._mem_store(key, val)

        return answer

if __name__ == '__main__':
    import doctest
    doctest.testmod()
