import sys
import os
import shutil
import shlex
import subprocess

builtin=["exit", "echo", "type"]
def execute_builtin(command_args):
    if command_args[0] == "exit":
        sys.exit()
    elif command_args[0] == "echo":
        [sys.stdout.write(args+" ") for args in command_args[1:]]
        print()
    elif command_args[0] == "type":
        if command_args[1] in builtin:
            print(f"{command_args[1]} is a shell builtin")
        else:
            if shutil.which(command_args[1]):
                print(f"{command_args[1]} is {shutil.which(command_args[1])}")
            else:
                print(f"{command_args[1]}: not found")
def main():
    while True:
        sys.stdout.write("$ ")
        full_command = input()
        command_args=shlex.split(full_command)
        if command_args[0] in builtin:
            execute_builtin(command_args)
        elif shutil.which(command_args[0]):
            subprocess.run(command_args)
        else:
            print(f"{command_args[0]}: command not found")



if __name__ == "__main__":
    main()
