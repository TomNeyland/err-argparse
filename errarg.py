import shlex
import argparse
from errbot import botcmd
from functools import wraps
import logging

log = logging.getLogger(__name__)

def option(*args, **kwargs):

    log.info('option called with: %s, %s', (args, kwargs))

    def option_decorator(func):

        if not hasattr(func, 'parser'):
            parser = argparse.ArgumentParser(description=func.__doc__)
            cmd_name = kwargs.pop('cmd_name', func.func_name)

            def wrapper(self, mess, cmd_args):
                cmd_args = shlex.split(cmd_args)
                cmd_namespace = parser.parse_args(cmd_args)
                cmd_kwargs = vars(cmd_namespace)
                return func(self, mess, **cmd_kwargs)

            wrapper.func_name = func.func_name
            wrapper.__doc__ = parser.format_help()
            wrapper = botcmd(name=cmd_name)(wrapper)
            wrapper.parser = parser
        else:
            wrapper = func

        log.info('add_argument called with: %s, %s', (args, kwargs))
        wrapper.parser.add_argument(*args, **kwargs)
        wrapper.__doc__ = wrapper.parser.format_help()

        return wrapper

    return option_decorator
