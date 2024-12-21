from rest_framework.exceptions import NotFound
from django.shortcuts import get_object_or_404


def get_object_or_raise_api_404(klass, *args, message="Resource not found", **kwargs):
    """
    Retrieve an object, or raise a 404 API Exception with a custom message.

    Parameters:
    - klass: The model class or queryset from which to retrieve the object.
    - message: Optional custom message for the NotFound exception (default is 'Resource not found').
    - *args, **kwargs: Arguments to filter the object.

    Returns:
    - The retrieved object if found, otherwise raises NotFound exception.
    """
    try:
        return get_object_or_404(klass, *args, **kwargs)
    except Exception:
        raise NotFound(detail=message)
