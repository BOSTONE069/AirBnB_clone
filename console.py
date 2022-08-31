#!/usr/bin/python3

import cmd
import sys
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage


class HBNBCommand(cmd.Cmd):
    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ''
    file = None

    className = {'BaseModel': BaseModel}

    def do_quit(self, arg):
        'Quit command to exit program'
        self.close()
        quit()
        return True

    def do_EOF(self, arg):
        """ Handles EOF to exit program """
        print()
        exit()

    def help_EOF(self):
        """ Prints the help documentation for EOF """
        print("Exits the program without formatting\n")

    def precmd(self, line):
        line = line.lower()
        if self.file and 'playback' not in line:
            print(line, file=self.file)
        return line

    def close(self):
        if self.file:
            self.file.close()
            self.file = None

    def do_create(self, arg):
        """Used in creation of class instance """
        if not arg:
            print("** class name missing **")
        elif arg not in HBNBCommand.className.keys():
            print("** class doesn't exist **")
        else:
            obj = HBNBCommand.className[arg]()
            HBNBCommand.className[arg].save(obj)
            print(obj.id)




def parse(arg):
    'Convert a series of zero or more numbers to an argument tuple'
    return tuple(map(int, arg.split()))


if __name__ == '__main__':
    HBNBCommand().cmdloop()
