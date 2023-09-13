from abc import ABCMeta

from threading import Lock


class SingletonMeta(type):
    """
    A metaclass that implements the Singleton pattern.

    This metaclass ensures that only one instance of a class is created and
    provides a global access point to that instance.

    Attributes:
        _instances (dict): A dictionary of class instances.
        _lock (Lock): A lock object for thread-safe instance creation.

    Methods:
        __call__(*args, **kwargs): Creates or returns the existing instance of
        the class.

    Usage:
        class MyClass(metaclass=SingletonMeta):
            ...
    """

    _instances = {}

    _lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                cls._instances[cls] = super().__call__(*args, **kwargs)

        return cls._instances[cls]


class ABCSingletonMeta(ABCMeta, SingletonMeta):
    pass
