"""elizastatementhandler.py -- Elize-like chatbot responses

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

class ElizaStatementHandler(StatementHandlerBase):
    """Handle statements that a pseudo Rogerian psychotherapist could answer"""
    PATTERNS = [('always', 'Can you think of a specific example?'),
                ('never', 'Not even once?'),
                ('my {topic}', "That's interesting."),
                ('what is a {topic}', "I have no clue."),
                ('what is an {topic}', "I have no clue."),
                ('they are', 'I never knew that.'),
                ('when do you', "I'm not in a rush."),
                ('when are you', "I take my time."),
                ('why are you', "I was born that way."),
                ('who are you', "Are you asking for my name?"),
                ('what are you', "I'm just like you."),
                ('where are you', "I live in the computer."),
                ('are you', 'Yes. How about you?'),
                ('you are', 'In what way exactly?')]

    def _pattern_match(self, statement, pattern):
        """Match pattern to statement, or return (False, None)

        >>> ElizaStatementHandler()._pattern_match("Are you smart?", 'are you')
        (True, None)

        >>> ElizaStatementHandler()._pattern_match("Are you smart?", 'you are')
        (False, None)

        >>> ElizaStatementHandler()._pattern_match('The weather was rainy today', 'the {topic} *')
        (True, 'weather')

        >>> ElizaStatementHandler()._pattern_match("He makes me so mad", 'he * me')
        (True, None)

        >>> ElizaStatementHandler()._pattern_match('My girlfriend said that', "my {topic} *")
        (True, 'girlfriend')
        """
        topic = None
        norm = statement.lower()

        for input_word, pattern_word in zip(norm.split(' '),
                                            pattern.split(' ')):
            if pattern_word == '*':
                pass
            elif pattern_word == '{topic}':
                topic = input_word
            elif pattern_word != input_word:
                return (False, None)
        return (True, topic)

    def can_handle(self, statement, memory):
        return self.handle(statement, memory) != None

    def handle(self, statement, memory):
        for pattern, answer in ElizaStatementHandler.PATTERNS:
            match, topic = self._pattern_match(statement, pattern)
            if match:
                mem = []
                if topic != None:
                    mem.append((MemoryKeys.key_topic(), topic))
                return Response(answer, mem)
        return None

if __name__ == '__main__':
    import doctest
    doctest.testmod()
