"""CPU functionality."""

import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # Create Memory
        self.ram = [0] * 256
        # Create Register
        self.reg = [0] * 8

        # Create program counter
        self.pc = 0

        # Running CPU is true
        self.running = True
        self.PC = self.reg[0]
        self.IM = self.reg[5]
        self.IS = self

    def LDI_function(self, a, b):
        self.reg[a] = b
        self.pc += 3

    def PRN_function(self, a):
        print(f'{self.reg[a]}')
        self.pc += 2

    def HLT_function(self):
        self.running = False
        self.pc += 1

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010,  # LDI R0,8 --> LOAD IMMEDIATELY
            0b00000000,  # R0
            0b00001000,  # 8
            0b01000111,  # PRN --> PRINT
            0b00000000,  # R0
            0b00000001,  # HLT --> STOP
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    # byte refers to the address

    def ram_read(self, byte):
        return self.ram[byte]

    # byte refers to the address
    # change refers to the new item to be added

    def ram_write(self, byte, change):
        self.ram[byte] = change
        return self.ram[byte]

    def run(self):
        """Run the CPU."""
        while self.running:
            # self.trace()
            # Setting current to IR
            ir = self.ram_read(self.pc)

            # Get PC+1
            operand_a = self.ram_read(self.pc+1)
            # Get PC+2
            operand_b = self.ram_read(self.pc+2)

            if ir == LDI:
                self.LDI_function(operand_a, operand_b)
            elif ir == PRN:
                self.PRN_function(operand_a)
            elif ir == HLT:
                self.running = False
            else:
                self.running = False
                print(f"I did not understand that ir: {ir}")
                sys.exit(1)
