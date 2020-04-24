"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # 256 bytes of RAM
        self.ram = [0] * 256
        # 8 bytes of general memory - register
        self.reg = [0] * 8
        # create the stack pointer at reg[7] and set value to F4 hex
        self.reg[7] = 0xf4
        # create a flag holder at reg[5] and set it to 0b00000000
        # last three binary digits will be L G E in that order
        self.reg[5] = 0b00000000
        # program counter value
        self.pc = 0
        # program on / off switch
        self.running = True

        # map variable names to function addresses
        self.command = {
            0b10000010: "LDI",
            0b01000111: "PRN",
            0b00000001: "HLT",
            0b10100010: "MUL",
            0b01000101: "PUSH",
            0b01000110: "POP",
            0b01010000: "CALL",
            0b00010001: "RET",
            0b10100000: "ADD",
            0b10100111: "CMP",
            0b01010100: "JMP",
            0b01010101: "JEQ",
            0b01010110: "JNE",
            0b10101000: "AND",
            0b10101010: "OR",
            0b10101011: "XOR",
            0b01101001: "NOT",
            0b10101100: "SHL",
            0b10101101: "SHR",
            0b10100100: "MOD",
            0b00011111: "ADDI"
        }
    
    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value
        return True

    def load(self, file):
        """Load a program into memory."""

        address = 0

        # open the file
        with open(file) as f:
            program = f.readlines()

        # clean out the comments and /n symbols
        for instruction in program:
            if "#" in instruction:
                instruction = instruction.split('#')[0]
            elif " #" in instruction:
                instruction = instruction.split(' #')[0]
            elif "\n" in instruction:
                instruction = instruction.split("\n")[0]

            # convert to binary and add the cleaned-up instructions into ram
            if len(instruction) > 0:
                instruction = int(instruction, 2)
                self.ram[address] = instruction
                address += 1
        
        # print(f"conversion complete, ram is {self.ram}")

    def alu(self, op, reg_a, reg_b=0):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]
        # LGE flag operations
        elif op == "CMP":
            # flags are stored 0b00000LGE - in that order
            if self.reg[reg_a] < self.reg[reg_b]:
                self.reg[5] = 0b00000100
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.reg[5] = 0b00000010
            elif self.reg[reg_a] == self.reg[reg_b]:
                self.reg[5] = 0b00000001
        # bitwise operations
        elif op == "AND":
            self.reg[reg_a] = self.reg[reg_a] & self.reg[reg_b]
        elif op == "OR":
            self.reg[reg_a] = self.reg[reg_a] | self.reg[reg_b]
        elif op == "XOR":
            self.reg[reg_a] = self.reg[reg_a] ^ self.reg[reg_b]
        elif op == "NOT":
            self.reg[reg_a] = ~self.reg[reg_a]
        elif op == "SHL":
            self.reg[reg_a] = self.reg[reg_a] << self.reg[reg_b]
        elif op == "SHR":
            self.reg[reg_a] = self.reg[reg_a] >> self.reg[reg_b]
        elif op == "MOD":
            self.reg[reg_a] = self.reg[reg_a] % self.reg[reg_b]
        # ADDI
        elif op == "ADDI":
            self.reg[reg_a] = self.reg[reg_a] + reg_b
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        while self.running:
            # instruction register
            ir = self.command[self.ram_read(self.pc)] # get the binary address of pc and convert it to the command
            # print(ir)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            # stop the program
            if ir == "HLT":
                self.running = False
            # set a register A to a value B
            elif ir == "LDI":
                self.reg[operand_a] = operand_b
                self.pc += 3
            # print A
            elif ir == "PRN":
                print(self.reg[operand_a])
                self.pc += 2
            elif ir == "MUL":
                self.alu("MUL", operand_a, operand_b)
                self.pc += 3
            elif ir == "ADD":
                self.alu("ADD", operand_a, operand_b)
                self.pc += 3
            elif ir == "PUSH":
                # decrement the stack pointer
                self.reg[7] -= 1
                # get address pointed to by SP
                sp = self.reg[7]
                # copy the value of the given register to that address
                self.ram[sp] = self.reg[operand_a]
                self.pc += 2
            elif ir == "POP":
                # get address pointed to by SP
                sp = self.reg[7]
                # copy the value of the given register to that address
                self.reg[operand_a] = self.ram[sp]
                # increment sp
                self.reg[7] += 1
                self.pc += 2
            elif ir == "CALL":
                # decrement the stack pointer
                self.reg[7] -= 1
                # get address pointed to by SP
                sp = self.reg[7]
                # copy the value of the return register to that address
                self.ram[sp] = self.pc + 2
                # jump to the given point in memory
                self.pc = self.reg[operand_a]
            elif ir == "RET":
                # get address pointed to by SP
                sp = self.reg[7]
                # put pc to that address
                self.pc = self.ram_read(sp)
                # increment sp (pop the stack)
                self.reg[7] += 1
            elif ir == "CMP":
                self.alu("CMP", operand_a, operand_b)
                self.pc += 3
            elif ir == "JMP":
                self.pc = self.reg[operand_a]
            elif ir == "JEQ":
                if self.reg[5] == 0b00000001:
                    self.pc = self.reg[operand_a] # jump if equal
                else:
                    self.pc += 2
            elif ir == "JNE":
                if self.reg[5] == 0b00000001:
                    self.pc += 2
                else:
                    self.pc = self.reg[operand_a] # jump if not equal
            # bitwise operations
            elif ir == "AND":
                self.alu("AND", operand_a, operand_b)
                self.pc += 3
            elif ir == "OR":
                self.alu("OR", operand_a, operand_b)
                self.pc += 3
            elif ir == "XOR":
                self.alu("XOR", operand_a, operand_b)
                self.pc += 3
            elif ir == "NOT":
                self.alu("NOT", operand_a)
                self.pc += 2 
            elif ir == "SHL":
                self.alu("SHL", operand_a, operand_b)
                self.pc += 3
            elif ir == "SHR":
                self.alu("SHR", operand_a, operand_b)
                self.pc += 3
            elif ir == "MOD":
                self.alu("MOD", operand_a, operand_b)
                self.pc += 3
            elif ir == "ADDI":
                self.alu("ADDI", operand_a, operand_b)
                self.pc += 3