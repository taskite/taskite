#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import subprocess


def run_npm_build():
    print("Building frontend assets...")
    try:
        subprocess.run(["npm", "run", "test:build"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to build frontend assets: {e}")
        sys.exit(1)


def main():
    """Run administrative tasks."""
    if "test" in sys.argv:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "taskite.settings.test")
        # run_npm_build()
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "taskite.settings.development")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
