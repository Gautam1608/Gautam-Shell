import sys


def main():
    command_list=["exit", "echo"]
    while True:
        sys.stdout.write("$ ")
        full_command = input()
        command_args=full_command.split(" ")[1:]
        command = full_command.split(" ")[0]
        if command in command_list:
            if command == "exit":
                sys.exit()
            elif command == "echo":
                [sys.stdout.write(args+" ") for args in command_args]
                print()
        else:
            print(f"{command}: command not found")



if __name__ == "__main__":
    main()
