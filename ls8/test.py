import sys

with open("./examples/print8.ls8") as f:
    program = f.readlines()

newarr = [0] * len(program)

for i in range(len(program)):
    if "#" in program[i]:
        newarr[i] = program[i].split("#")[0]
    elif " #" in program[i]:
        newarr[i] = program[i].split(" #")[0]
    elif "\n" in program[i]:
        newarr[i] = program[i].split("\n")[0]
    else:
        newarr[i] = program[i]

print(newarr)