#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

from .signals import Signal

__all__ = ["Manager"]

logger = logging.getLogger(__name__)


class Manager(object):
    """
    A base class to manage objects needing to be registered, and to inform
    other objects of their creation, deletion, etc.
    """
    def __init__(self):
        """
        Create containers and signals.
        """
        # containers
        self.availables = {}
        self.instances = []
        self.instancesByName = {}

        # signals
        self.added = Signal()
        self.created = Signal()
        self.deleted = Signal()

    def add(self, name, cls):
        """
        Add a class to the register.
        """
        # check presence of the class or not
        if name in self.availables:
            logger.error("Class {0} already available".format(name))
            raise ValueError(
                "The class {0} is already defined".format(name)
            )

        # make the class available
        logger.debug("Class {0} now available".format(name))
        self.availables[name] = cls

        # send a signal with the name and the class
        self.added(name, cls)

    def create(self, instance):
        """
        Register created instance.
        """
        # register it
        logger.debug("Registering instance {0}".format(instance))
        self.instances.append(instance)
        if hasattr(instance, "name"):
            self.instancesByName[instance.name] = instance

        # send signal created
        self.created(instance)

    def delete(self, instance):
        """
        Unregister an instance.
        """
        # remove the instance from the manager
        logger.debug("Unregistering instance {0}".format(instance))
        self.instances.remove(instance)
        self.instancesByName.pop(instance.name, None)

        # send a signal that it has been deleted
        self.deleted(instance)

    def __getitem__(self, name):
        """
        Get an instance from the manager given only its name, as it was a
        dictionary.
        """
        return self.instancesByName[name]

    def __contains__(self, name):
        """
        Check if the manager contains a given instance by its name.
        """
        return name in self.instancesByName


# vim: set tw=79 :
