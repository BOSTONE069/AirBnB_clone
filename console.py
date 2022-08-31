#!/usr/bin/python3

import cmd
import sys

class HBNBCommand(cmd.Cmd):
    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ''
    file = None

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

def parse(arg):
    'Convert a series of zero or more numbers to an argument tuple'
    return tuple(map(int, arg.split()))

if __name__ == '__main__':
   HBNBCommand().cmdloop()
