#!/usr/bin/python3
"""This is the file storage class"""
import json
from models.base_model import BaseModel


class FileStorage:
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """returns the dictionary __objects"""
        return FileStorage.__objects

    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id"""
        keyobj = obj.__class__.__name__
        FileStorage.__objects["{}.{}".format(keyobj, obj.id)] = obj

    def save(self):
        """serializes __objects to the JSON file (path: __file_path)"""
        obdict = FileStorage.__objects
        objdict = {obj: obdict[obj].to_dict() for obj in obdict.keys()}
        with open(FileStorage.__file_path, "w") as f:
            json.dump(objdict, f)

    def reload(self):
        """Deserialize the JSON file __file_path to __objects, if it exists."""
        try:
            with open(FileStorage.__file_path) as f:
                objdict = json.load(f)
                for o in objdict.values():
                    cls_name = o["__class__"]
                    del o["__class__"]
                    self.new(eval(cls_name)(**o))
        except FileNotFoundError:
            return

