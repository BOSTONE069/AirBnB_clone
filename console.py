#!/usr/bin/python3

import cmd
import re
import sys
from shlex import split

from models.base_model import BaseModel
from models import storage
from models.user import User


def parse(arg):
    curly_braces = re.search(r"\{(.*?)\}", arg)
    brackets = re.search(r"\[(.*?)\]", arg)
    if curly_braces is None:
        if brackets is None:
            return [i.strip(",") for i in split(arg)]
        else:
            lexer = split(arg[:brackets.span()[0]])
            retl = [i.strip(",") for i in lexer]
            retl.append(brackets.group())
            return retl
    else:
        lexer = split(arg[:curly_braces.span()[0]])
        retl = [i.strip(",") for i in lexer]
        retl.append(curly_braces.group())
        return retl


class HBNBCommand(cmd.Cmd):
    prompt = '(hbnb) '

    className = {'BaseModel': BaseModel,
                 'User': User}

    def do_quit(self, arg):
        """Quit command to exit program"""
        return True

    def do_EOF(self, arg):
        """ Handles EOF to exit program """
        print()
        exit()

    def help_EOF(self):
        """ Prints the help documentation for EOF """
        print("Exits the program without formatting\n")

    def do_create(self, arg):
        """Used in creation of class instance """

        arglength = parse(arg)
        if len(arglength) == 0:
            print("** class name missing **")
        elif arglength[0] not in HBNBCommand.className.keys():
            print("** class doesn't exist **")
        else:
            print(eval(arglength[0])().id)
            storage.save()

    def do_show(self, arg):
        """
        Usage: show <class> <id> or <class>.show(<id>)
        Display the string representation of a class instance of a given id.
        """
        arglength = parse(arg)
        objdict = storage.all()
        if len(arglength) == 0:
            print("** class name missing **")
        elif arglength[0] not in HBNBCommand.className.keys():
            print("** class doesn't exist **")
        elif len(arglength) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(arglength[0], arglength[1]) not in objdict:
            print("** no instance found **")
        else:
            print(objdict["{}.{}".format(arglength[0], arglength[1])])

    def do_destroy(self, arg):
        """Usage: destroy <class> <id> or <class>.destroy(<id>)
        Delete a class instance of a given id."""
        arglength = parse(arg)
        objdict = storage.all()
        if len(arglength) == 0:
            print("** class name missing **")
        elif arglength[0] not in HBNBCommand.className.keys():
            print("** class doesn't exist **")
        elif len(arglength) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(arglength[0], arglength[1]) not in objdict.keys():
            print("** no instance found **")
        else:
            del objdict["{}.{}".format(arglength[0], arglength[1])]
            storage.save()

    def do_all(self, arg):
        """
        It prints all the string representation of all the objects in the storage.

        :param arg: the string that the user inputs
        """
        arglength = parse(arg)
        if len(arglength) > 0 and arglength[0] not in HBNBCommand.className.keys():
            print("** class doesn't exist **")
        else:
            objlength = []
            for obj in storage.all().values():
                if len(arglength) > 0 and arglength[0] == obj.__class__.__name__:
                    objlength.append(obj.__str__())
                elif len(arglength) == 0:
                    objlength.append(obj.__str__())
            print(objlength)

    def do_update(self, arg):
        """
        This function updates an
        instance based on the class name and id by adding or updating attribute (save the change
        into the JSON file)
        """
        arglength = parse(arg)
        objdict = storage, all()

        if len(arglength) == 0:
            print("** class name missing **")
            return False
        if arglength[0] not in HBNBCommand.className.keys():
            print("** class doesn't exist **")
            return False
        if len(arglength) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(arglength[0], arglength[1]) not in objdict.keys():
            print("** no instance found **")
            return False
        if len(arglength) == 2:
            print("** attribute name missing **")
            return False
        if len(arglength) == 3:
            try:
                type(eval(arglength[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(arglength) == 4:
            obj = objdict["{}.{}".format(arglength[0], arglength[1])]
            if arglength[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[arglength[2]])
                obj.__dict__[arglength[2]] = valtype(arglength[3])
            else:
                obj.__dict__[arglength[2]] = arglength[3]
        elif type(eval(arglength[2])) == dict:
            obj = objdict["{}.{}".format(arglength[0], arglength[1])]
            for k, v in eval(arglength[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    valtype = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = valtype(v)
                else:
                    obj.__dict__[k] = v
        storage.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
