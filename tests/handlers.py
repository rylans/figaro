"""handlers.py -- Dynamic tests to ensure that handlers conform to spec"""

from __future__ import print_function

import os
import json

def check_can_handle(handler_init, can_handle_str):
    """Verify that handler can handle the expected string"""
    assert handler_init().can_handle(can_handle_str, {}) == True, \
            '%s failed to handle "%s"' % (handler_init.__name__, can_handle_str)

def check_not_handle(handler_init, not_handle_str):
    """Verify that handler can not handle the given string"""
    assert handler_init().can_handle(not_handle_str, {}) == False, \
            '%s expected to not be able to handle "%s"' % (handler_init.__name__, not_handle_str)

def build_specific(handler_callable):
    handler_name = handler_callable.__name__
    handlers_data_path = os.path.join('tests', 'handlers_data')
    data_file = os.path.join(handlers_data_path, handler_name + '.json')

    with open(data_file, 'r') as data_fp:
        try:
            test_data = json.load(data_fp)
        except Exception as e:
            print("Error loading %s" % data_file)
            raise e

    try:
        can_handle = test_data['can_handle']
        not_handle = test_data['not_handle']
    except KeyError as keye:
        print("Unable to load key from json %s" % data_file)
        raise keye

    def test():
        check_can_handle(handler_callable, can_handle)
        check_not_handle(handler_callable, not_handle)
    return test

def check_all_handlers():
    from figaro import *
    localdict = locals().copy()
    handlerkeys = [k for k in localdict if "Handler" in k]
    handlertests = [build_specific(localdict[k]) for k in handlerkeys]

    errors = []

    for t in handlertests:
        try:
            t()
        except AssertionError as e:
            errors.append(e)

    if errors:
        print(errors)
        raise errors[0]

if __name__ == '__main__':
    check_all_handlers()
