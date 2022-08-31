#!/usr/bin/python3

import cmd
import sys


class HBNBCommand(cmd.Cmd):
    """It's a class that inherits from the Cmd class."""
    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ''
    file = None

    def do_quit(self, arg):
        """
        The function do_quit() is a method of the class Cmd.
        It takes two arguments, self and arg. The docstring is a string
        that is printed when the user types help quit. The function returns True

        :param arg: The argument passed to the command
        :return: True
        """
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
        """
        It takes the command line input,
        converts it to lowercase, and
        then prints it to the file if the file is open

        :param line: The line that the user has entered
        :return: The line is being returned.
        """
        line = line.lower()
        if self.file and 'playback' not in line:
            print(line, file=self.file)
        return line

    def close(self):
        """
        It closes the file if it is open
        """
        if self.file:
            self.file.close()
            self.file = None


def parse(arg):
    'Convert a series of zero or more numbers to an argument tuple'
    return tuple(map(int, arg.split()))


if __name__ == '__main__':
    HBNBCommand().cmdloop()
