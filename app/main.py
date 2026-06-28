import sys


def main():
    command_list=["exit"]
    while True:
        sys.stdout.write("$ ")
        command = input()
        if command.split(" ")[0] in command_list:
            sys.exit()
        else:
            print(f"{command.split(" ")[0]}: command not found")



if __name__ == "__main__":
    main()
