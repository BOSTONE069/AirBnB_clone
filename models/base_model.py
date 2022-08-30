#!/usr/bin/python3
"""Defines the BaseModel class"""
import models
from uuid import uuid4
from datetime import datetime


class BaseModel:
    """This is the class that represents the BaseModel"""
    def __init__(self, *arg, **kwargs):
        """
        It creates a new instance of the class.
        """
        tformat = "%Y-%m-%dT%H:%M:%S.%f"
        self.id = str(uuid4())
        self.created_at = datetime.today()
        self.updated_at = datetime.today()
        if len(kwargs) != 0:
            for j, k in kwargs.items():
                if j == "created_at" or j == "updated_at":
                    self.__dict__[j] = datetime.strptime(k, tformat)
                else:
                    self.__dict__[j] = k
        else:
            models.storage.new(self)

    def save(self):
        """
        The save function updates the updated_at attribute of the
        instance with the current datetime and saves the instance
        to the JSON file
        """
        self.updated_at = datetime.today()
        models.storage.save()

    def to_dict(self):
        """
        This function takes an object and returns a
        dictionary representation of that object
        :return: The return_dict is being returned.
        """
        return_dict = self.__dict__.copy()
        return_dict["created_at"] = self.created_at.isoformat()
        return_dict["updated_at"] = self.updated_at.isoformat()
        return_dict["__class__"] = self.__class__.__name__
        return return_dict

    def __str__(self):
        """
        The function returns a string that contains the class name,
        the id of the object, and the contents of the object's
        dictionary
        :return: The class name, the id of the object, and the dictionary of the object.
        """
        clname = self.__class__.__name__
        return "{} {} {}".format(clname, self.id, self.__dict__)
