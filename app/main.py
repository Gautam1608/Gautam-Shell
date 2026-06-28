import sys
import os
import shutil
import shlex
import subprocess

builtin=["exit", "echo", "type"]
def execute_builtin(tokens):
    if tokens[0] == "exit":
        sys.exit()
    elif tokens[0] == "echo":
        [sys.stdout.write(args+" ") for args in tokens[1:]]
        print()
    elif tokens[0] == "type":
        if tokens[1] in builtin:
            print(f"{tokens[1]} is a shell builtin")
        else:
            if shutil.which(tokens[1]):
                print(f"{tokens[1]} is {shutil.which(tokens[1])}")
            else:
                print(f"{tokens[1]}: not found")
def main():
    while True:
        sys.stdout.write("$ ")
        raw_input = input()
        tokens=shlex.split(raw_input)
        if tokens[0] in builtin:
            execute_builtin(tokens)
        elif shutil.which(tokens[0]):
            subprocess.run(tokens)
        else:
            print(f"{tokens[0]}: command not found")



if __name__ == "__main__":
    main()
