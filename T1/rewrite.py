from ast import *
from core.transformers import rewrite
from core.transformers import RewriterCommand
from core.util import *
from pathlib import Path
import os
import sys



args = sys.argv
if len(args) < 2:
    print("Incomplete Command")

targetFile = sys.argv[1]
path = Path(targetFile)
fileContent = open(targetFile).read()

if not path.is_file():
    print("File not exists")

commandName = sys.argv[0]
commands = select(lambda cmd: commandName in cmd.name(), RewriterCommand.__subclasses__())

if len(commands) < 1:
    print("Command not found")

output = rewrite(commands[0], fileContent)
print(output)
