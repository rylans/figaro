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
from math import log, log10, sqrt, sin, cos, tan
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

class DeclarationHandler(StatementHandlerBase):
    """Handle delcarative statements"""
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

class ArithmeticHandler(StatementHandlerBase):
    """Class for basic arithmetic responses"""
    _ADD = lambda x, y: sum([x, y])
    _SUBTRACT = lambda x, y: sum([x, -1*y])
    _PRODUCT = lambda x, y: x*y

    INFIX_OPS = [('+', _ADD),
                 ('plus', _ADD),
                 ('-', _SUBTRACT),
                 ('minus', _SUBTRACT),
                 ('*', _PRODUCT),
                 ('times', _PRODUCT)]

    UNARY_OPS = [('root', sqrt),
                 ('sqrt', sqrt),
                 ('sin', sin),
                 ('cos', cos),
                 ('tan', tan),
                 ('ln', log),
                 ('log', log10)]

    def _is_number_in(self, tokens):
        """Return true if there is a number available

        >>> ArithmeticHandler()._is_number_in('5 of them'.split(' '))
        True
        """
        for token in tokens:
            try:
                return float(token) != None
            except ValueError:
                pass
        return False

    def _has_number_after(self, tokens, ix):
        """Check if number occurs after given index

        >>> ArithmeticHandler()._has_number_after("give me log of 7".split(), 3)
        True

        >>> ArithmeticHandler()._has_number_after("what is 7 log of?".split(), 3)
        False
        """
        def try_parse_float(x):
            try:
                return float(x)
            except ValueError:
                return None
        return any([try_parse_float(x) for x in tokens[ix:]])

    def _has_infix(self, statement):
        """Return true if it is able to handle infix operation

        >>> ArithmeticHandler()._has_infix("calculate 5 plus 2")
        True

        >>> ArithmeticHandler()._has_infix("calculate + 2 please")
        False
        """
        tokens = statement.split(' ')
        for ix, token in enumerate(tokens):
            for op, _ in ArithmeticHandler.INFIX_OPS:
                if op == token:
                    return self._is_number_in(tokens[ix:]) and self._is_number_in(tokens[:ix])
        return False

    def _has_unary(self, statement):
        """Return true if unary statement can be handled

        >>> ArithmeticHandler()._has_unary('what is square root of 5')
        True

        >>> ArithmeticHandler()._has_unary('what is square root of')
        False

        >>> ArithmeticHandler()._has_unary('root 64.0')
        True

        >>> ArithmeticHandler()._has_unary('what is 12 of 5')
        False
        """
        tokens = statement.split(' ')
        for ix, token in enumerate(tokens):
            for op, _ in ArithmeticHandler.UNARY_OPS:
                if op == token:
                    return self._is_number_in(tokens[ix:])
        return False

    def _calc_unary(self, statement):
        """Return output of unary operation

        >>> ArithmeticHandler()._calc_unary('what is root of 16')
        4.0

        >>> ArithmeticHandler()._calc_unary('calculate log 100')
        2.0

        >>> ArithmeticHandler()._calc_unary('you know what square root of 64 is?')
        8.0
        """
        tokens = statement.split(' ')
        op_func = None
        start_ix = 0
        arg = None
        for ix, token in enumerate(tokens):
            for op_word, func in ArithmeticHandler.UNARY_OPS:
                if op_word == token:
                    op_func = func
                    start_ix = ix
        for token in tokens[start_ix:]:
            try:
                number = float(token)
                arg = number
                break
            except ValueError:
                pass

        if op_func == None or arg == None:
            raise RuntimeError("Unable to calculate unary operation: %s" % statement)
        return op_func(arg)

    def _calc_infix(self, statement):
        """Return output of infix operation

        >>> ArithmeticHandler()._calc_infix('7 + 2')
        9.0

        >>> ArithmeticHandler()._calc_infix('tell me 20 minus 48')
        -28.0
        """
        tokens = statement.split(' ')
        op_func = None
        start_ix = 0
        arg_a = None
        arg_b = None
        for ix, token in enumerate(tokens):
            for op_word, func in ArithmeticHandler.INFIX_OPS:
                if op_word == token:
                    op_func = func
                    start_ix = ix

        for token in tokens[start_ix:]:
            try:
                number = float(token)
                arg_b = number
                break
            except ValueError:
                pass

        for token in tokens[:start_ix]:
            try:
                number = float(token)
                arg_a = number
                break
            except ValueError:
                pass

        if op_func == None or arg_a == None or arg_b == None:
            raise RuntimeError("Unable to calculate operation: %s" % statement)
        return op_func(arg_a, arg_b)

    def can_handle(self, statement, memory=None):
        low = statement.lower()
        return self._has_infix(low) or self._has_unary(low)

    def handle(self, statement, memory=None):
        """Respond to basic arithmetic request

        >>> ArithmeticHandler().handle("compute 4 * -2").answer
        '-8.0'

        >>> ArithmeticHandler().handle("3.0 times 9.0").answer
        '27.0'

        >>> ArithmeticHandler().handle("What is 13 - 20").answer
        '-7.0'

        >>> ArithmeticHandler().handle("Calculate for me square root of 100").answer
        '10.0'
        """
        if self._has_unary(statement):
            num = self._calc_unary(statement)
            return Response(str(num), [])
        elif self._has_infix(statement):
            num = self._calc_infix(statement)
            return Response(str(num), [])
        raise RuntimeError("ArithmeticHandler reported ability to handle %s but can't" % statement)

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
