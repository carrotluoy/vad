"""Least-Privilege Prompt entry; legacy verifier modes have been retired."""
import importlib
if __name__ == '__main__':
    importlib.import_module((__package__ + '.' if __package__ else '') + 'policy_only_runner').main('least_privilege_prompt')
