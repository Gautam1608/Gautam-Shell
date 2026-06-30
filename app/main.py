import sys
import os
import shutil
import shlex
import subprocess
from pathlib import Path

try:
    import readline
except ImportError:
    try:
        from pyreadline3 import Readline
        readline = Readline()
        def input(txt):
            readline.readline(txt)
    except ImportError:
        readline = None


builtin=["exit", "echo", "type", "pwd","cd"]
autocomplete_list=builtin.copy()
for path in os.environ.get("PATH", "").split(os.pathsep):
    if os.path.exists(path):
        autocomplete_list.extend(os.listdir(path))


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

def redirect_output(tokens):
    if ">" in tokens or "1>" in tokens:
        i = tokens.index("1>" if "1>" in tokens else ">") + 1
        sys.stdout = open(tokens[i],'w')
        return tokens[:i-1]
    elif "2>" in tokens:
        i = tokens.index("2>") + 1
        sys.stderr = open(tokens[i],'w')
        return tokens[:i-1]
    elif ">>" in tokens or "1>>" in tokens:
        i = tokens.index("1>>" if "1>>" in tokens else ">>") + 1
        sys.stdout = open(tokens[i],'a')
        return tokens[:i-1]
    elif "2>>" in tokens:
        i = tokens.index("2>>") + 1
        sys.stderr = open(tokens[i],'a')
        return tokens[:i-1]
    return tokens
def reset_output():
    sys.stderr=sys.__stderr__
    sys.stdout=sys.__stdout__

def completer(text,state):
    buffer = readline.get_line_buffer()
    last_word = buffer.split()[-1] if buffer else ""
    prev_path = Path(last_word)
    if not prev_path.is_dir():
        prev_path = Path()
    if not text:
        options=([cmd for cmd in os.listdir(prev_path)])
    else:
        if '/' not in text and '\\' not in text:
            options = [cmd for cmd in autocomplete_list if cmd.startswith(text)]
            options.extend([cmd for cmd in os.listdir() if cmd.startswith(text)])
        else:
            path = prev_path/Path(text)
            prefix = "./" if not path.is_absolute() else ""
            if path.is_dir():
                options = [prefix+str(path/cmd).as_posix() for cmd in os.listdir(path)]
            else:
                path_dir = path.parent.absolute()
                path_text = path.name
                options = [(path.parent/cmd).as_posix() for cmd in os.listdir(path_dir) if cmd.startswith(path_text)]
    if state < len(options):
        option = Path(options[state])
        if option.is_dir():
            return option.as_posix()+"/"
        return options[state]+" "
    return None

def main():
    readline.set_completer(completer)
    readline.parse_and_bind("tab: complete")
    while True:
        try:
            reset_output()
            raw_input = input("$ ")
            tokens=redirect_output(shlex.split(raw_input)) 
            local_path = os.path.join(os.getcwd(), tokens[0])
            if not tokens:
                continue   
            if tokens[0] in builtin:
                execute_builtin(tokens)
            elif shutil.which(tokens[0]):
                subprocess.run(tokens, stdout= sys.stdout, stderr=sys.stderr)
            elif os.path.isfile(local_path) and os.access(local_path, os.X_OK):
                subprocess.run(local_path, stdout= sys.stdout, stderr=sys.stderr)
            else:
                print(f"{tokens[0]}: command not found")
        except KeyboardInterrupt:
            print()


if __name__ == "__main__":
    main()
