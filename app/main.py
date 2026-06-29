import sys
import os
import shutil
import shlex
import subprocess

builtin=["exit", "echo", "type", "pwd","cd"]
def execute_builtin(tokens):
     match tokens[0]:
        case "exit":
             sys.exit()
        case "echo":
            [sys.stdout.write(args+" ") for args in tokens[1:]]
            print()
        case "type":
            if tokens[1] in builtin:
                print(f"{tokens[1]} is a shell builtin")
            else:
                if shutil.which(tokens[1]):
                    print(f"{tokens[1]} is {shutil.which(tokens[1])}")
                else:
                    print(f"{tokens[1]}: not found")
        case "pwd":
            print(os.getcwd())
        case "cd":
            try:
                hpath = os.path.expanduser(tokens[1])
                os.chdir(hpath)
            except FileNotFoundError as e:
                print(f"cd: {hpath}: No such file or directory")
def main():
    while True:
        try:
            sys.stdout = sys.__stdout__
            sys.stdout.write("$ ")
            raw_input = input()
            tokens=shlex.split(raw_input)
            if ">" in tokens or "1>" in tokens:
                i = tokens.index(f"{"1"*("1>" in tokens)}>") + 1
                sys.stdout = open(tokens[i],'w')
                tokens = tokens[:i-1]
            if tokens[0] in builtin:
                execute_builtin(tokens)
            elif shutil.which(tokens[0]):
                subprocess.run(tokens, stdout= sys.stdout)
            else:
                print(f"{tokens[0]}: command not found")
        except KeyboardInterrupt:
            print()


if __name__ == "__main__":
    main()
