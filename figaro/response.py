"""response.py -- handler response model

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
        self._term = False

    def terminate_conversation(self):
        """Signal end of conversation"""
        self._term = True
        return self

    @property
    def terminated(self):
        """True if conversation should be ended"""
        return self._term

    @property
    def answer(self):
        """The textual response to the inquiry"""
        return self._answer

    @property
    def memo(self):
        """The facts to memorize"""
        return self._memo

    def __repr__(self):
        return "<Response '%s'>" % self.answer

if __name__ == '__main__':
    import doctest
    doctest.testmod()
