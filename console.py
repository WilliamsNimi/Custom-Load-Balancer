"""
Contains the entry point of the command interpreter
"""
import cmd
import csv
import os
import re
import sys


class HBNBCommand(cmd.Cmd):

    intro = "Welcome to the Load Balancer Console. Type help to view various help topics"
    prompt = "(Custom_LB:) "

    def help_configure(self):
        print("Type configure to configure the load balance by providing IPs and Ports")

    def help_start(self):
        print("Type start to start the load balancer server")

    def help_quit(self):
        print('Exit the program')

    def help_EOF(self):
        print("EOF command to exit the program")

    def emptyline(self):
        """ Executes no command when no input is entered """
        pass

    def do_configure(self, arg):
        print("Enter Server IP and Port. Enter 1 as value for both Server and port to terminate")
        server = "0"
        while server != "1":
            server = input("Server:")
            port = input("Port:")
            if server != "1" and port != "1":
                with open("servers_config.csv", 'a') as file:
                    writer = csv.writer(file, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow((server, port))
        print("Configuration complete")

    def do_start(self, arg):
        os.system("sudo python3 LoadBalancer.py")
    
    def do_EOF(self, line):
        """Handles EOF (Ctrl+C or Ctrl+Z) by exiting the console"""
        sys.exit(1)

    def do_quit(self, line):
        """ Quit command to exit the program """
        sys.exit(1)

if __name__ == '__main__':
    HBNBCommand().cmdloop()
