#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .manager import Manager

__all__ = [
    "Singleton", "SingletonManager", "ManagerMeta"
]


class Singleton(type):
    """
    A metaclass to create singletons, i.e classes that can have at most only
    one instance created at a given time.
    """
    def __call__(cls, *args, **kwargs):
        """
        Check that an instance is already stored before creating a new one.
        """
        if hasattr(cls, "instance"):
            return cls.instance

        cls.instance = super(Singleton, cls).__call__(*args, **kwargs)

        return cls.instance


class ManagerMeta(type):
    """
    A metaclass to allow simple managing of instances.
    """
    def __new__(cls, name, bases, attr, **kwargs):
        """
        Overridden to remove the keyword arguments coming from the class
        definition, after the metaclass keyword. They can be retrieved as
        keyword arguments in the metaclass provided for the class construction,
        but the default metaclass (type) doesn't handle keyword arguments, so
        we need to remove them before sending it to type.
        """
        return super(ManagerMeta, cls).__new__(cls, name, bases, attr)

    def __init__(
        cls,
        name,
        bases,
        attr,
        manager=Manager,
        after_creation=lambda x, y: None,
    ):
        """
        To initiate the manager of connectors.
        """
        # init the class as usual
        super(ManagerMeta, cls).__init__(name, bases, attr)

        # add a manager of the connectors
        if not hasattr(cls, "manager"):
            # check if a manager is given at the construction of the class
            cls.manager = manager()
            return

        # do something after the class creation
        after_creation(cls, name)

        # also add the class to the manager
        cls.manager.add(name, cls)

    def __call__(cls, *args, **kwargs):
        """
        Register the database when the instance of the database is created.
        """
        # create the instance
        instance = super(ManagerMeta, cls).__call__(*args, **kwargs)

        # register the database
        cls.manager.create(instance)

        return instance


class SingletonManager(ManagerMeta):
    """
    Metaclass to manage instances created with a given name as singletons.
    """
    def __call__(cls, name, *args, **kwargs):
        """
        Check instance already created, else create one and register.
        """
        # check if the instance already exists
        if name in cls.manager:
            return cls.manager[name]

        # create the instance as usual and register it
        return super(SingletonManager, cls).__call__(
            name,
            *args,
            **kwargs
        )


# vim: set tw=79 :
