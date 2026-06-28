import sys


def main():
    commands=[]
    sys.stdout.write("$ ")
    x = input()
    if x.split(" ")[0] in commands:
        ...
    else:
        sys.stdout.write(x.split()[0] + ": command not found")


if __name__ == "__main__":
    main()
