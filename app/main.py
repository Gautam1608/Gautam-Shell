import sys
import os

def main():
    builtin=["exit", "echo", "type"]
    while True:
        sys.stdout.write("$ ")
        full_command = input()
        command_args=full_command.split(" ")[1:]
        command = full_command.split(" ")[0]
        if command in builtin:
            if command == "exit":
                sys.exit()
            elif command == "echo":
                [sys.stdout.write(args+" ") for args in command_args]
                print()
            elif command == "type":
                if command_args[0] in builtin:
                    print(f"{command_args[0]} is a shell builtin")
                else:
                    paths = os.environ['PATH']
                    path_list = paths.split(os.pathsep)
                    for path in path_list:
                        if os.access(os.path.join(path,command_args[0]), os.X_OK):
                            print(f"{command_args[0]} is {os.path.join(path,command_args[0])}")
                            break
                    else:
                        print(f"{command_args[0]}: not found")
        else:
            print(f"{command}: command not found")



if __name__ == "__main__":
    main()
