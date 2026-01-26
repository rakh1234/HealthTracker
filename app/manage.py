#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    # Add parent directory to sys.path so we can import 'app.settings'
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
    
    # Use environment variable if set, otherwise default to 'app.settings'
    if 'DJANGO_SETTINGS_MODULE' not in os.environ:
        os.environ['DJANGO_SETTINGS_MODULE'] = 'app.settings'
    
    # Verify we can import the settings module
    try:
        import importlib
        importlib.import_module(os.environ['DJANGO_SETTINGS_MODULE'])
    except ImportError as e:
        print(f"Error: Cannot import {os.environ['DJANGO_SETTINGS_MODULE']}")
        print(f"Current directory: {os.getcwd()}")
        print(f"Parent directory: {parent_dir}")
        print(f"sys.path: {sys.path}")
        raise
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
