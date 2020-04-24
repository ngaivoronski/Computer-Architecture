import sys
import inspect

# with open("./examples/print8.ls8") as f:
#     program = f.readlines()

# newarr = [0] * len(program)

# for i in range(len(program)):
#     if "#" in program[i]:
#         newarr[i] = program[i].split("#")[0]
#     elif " #" in program[i]:
#         newarr[i] = program[i].split(" #")[0]
#     elif "\n" in program[i]:
#         newarr[i] = program[i].split("\n")[0]
#     else:
#         newarr[i] = program[i]

def testfunc(x,y,z):
    return x+y+z

def testfunc2(x, y):
    return x+y

print(testfunc2.__code__.co_argcount)