"""Vanilla entry: seven scenarios and fixed paper protocol."""
import importlib
if __name__ == '__main__':
    importlib.import_module((__package__ + '.' if __package__ else '') + 'policy_only_runner').main('vanilla')
