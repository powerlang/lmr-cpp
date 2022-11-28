# Copyright (c) 2020 Javier Pimas & LabWare
#
# This program and the accompanying materials are made available under
# the terms of the MIT license, see LICENSE file.
#
# SPDX-License-Identifier: MIT

"""
This module contains GDB CLI commands and convenience variables/functions
"""

import re

import gdb

from itertools import chain

from powerlang.printing import obj
from powerlang.objectmemory import segments

flatten = chain.from_iterable


class __DumpObjectCmd(gdb.Command):
    """
    Dump contents or expression EXP
    Usage: do EXP [EXP...]

    An expression EXP can be either OOP as numerical constant
    (for example '0x1ff10028') or C/C++ expression which is
    evaluated in current frame (for example, 'kernel->header.module')
    """
    def invoke (self, args, from_tty):
        self(*gdb.string_to_argv(args))

    def __call__(self, *exprs):
        for expr in exprs:
            self.dump(expr)

    def complete(self, text, word):
        return gdb.COMPLETE_EXPRESSION

    def dump(self, expr):
        o = None
        try:
            o = obj(expr)
        except:
            print("Failed to evaluate '%s'" % expr)
            return

        print(str(o))
        if not o.isBytes():
            for name, value in o.children():
                pp = gdb.default_visualizer(value)
                if pp == None:
                    print("    %-15s:  %s" % ( name , value ))
                else:
                    print("    %-15s:  %s" % ( name , pp.to_string() ))


do = __DumpObjectCmd('do', gdb.COMMAND_DATA)

class __LookupSymbol(gdb.Command):
    """
    Looks up a method containing given PC or matching given REGEXP.
    Usage: ls [PC]
           ls REGEXP

    PC can be given as an expression evaluating to an address
    or omitted in which case value if $pc (PC of currently
    selected frame) is used.

    If REGEXP is given, all methods whose name matches
    given regexp are looked up and printed.
    """
    def invoke(self, args, from_tty):
        argv = gdb.string_to_argv(args)
        if len(argv) > 1:
            raise Exception("lm takes only one argument (%d given)" % len(argv))
        elif len(argv) == 0:
            argv = ['$pc']
        any_found = False
        for symbol in self(argv[0]):
            any_found = True
            print(symbol)
        if not any_found:
            print("No symbol found.")

    def __call__(self, pc_or_regexp = '$pc'):
        pc = None
        regexp = None
        try:
            pc = None
            if isinstance(pc_or_regexp, int):
                pc = pc_or_regexp
            elif isinstance(pc_or_regexp, gdb.Value):
                pc = int(pc)
            elif isinstance(pc_or_regexp, str):
                pc = gdb.parse_and_eval(pc_or_regexp)
            else:
                raise InvalidArgument("pc_or_regexp must be an int, str, or gdb.Value")
        except:
            regexp = re.compile(pc_or_regexp)

        symtabs = [ segment.symtab for segment in segments ]

        if pc != None:
            for symtab in symtabs:
                sym = symtab.lookup_symbol_by_addr(pc)
                if sym != None:
                    return [sym]
            return []
        if regexp != None:
            return (sym for sym in flatten(symtabs) if regexp.search(sym.name))

ls = __LookupSymbol('ls', gdb.COMMAND_DATA)

class __DisassembleSymbol(gdb.Command):
    """
    Disassemble a symbol with given PC or matching given REGEXP.
    Usage: ls [PC]
           ls REGEXP

    PC can be given as an expression evaluating to an address
    or omitted in which case value if $pc (PC of currently
    selected frame) is used.

    If REGEXP is given then method matching that REGEXP is
    disassembled
    """
    def invoke(self, args, from_tty):
        argv = gdb.string_to_argv(args)
        if len(argv) > 1:
            raise Exception("as takes only one argument (%d given)" % len(argv))
        elif len(argv) == 0:
            argv = ['$pc']
        self(argv[0])

    def __call__(self, pc_or_regexp = '$pc'):
        syms = list(ls(pc_or_regexp))
        if len(syms) == 0:
            print("No symbol matching %s" % pc_or_regexp)
        elif len(syms) > 1:
            print("Multiple symbols matching %s:" % pc_or_regexp)
            for methodsym in syms:
                print(methodsym)
            print("Please disambiguate")
        else:
            self.disassemble(syms[0])


    def disassemble(self, sym):
        arch = gdb.selected_inferior().architecture()
        loPC = sym.address
        hiPC = loPC + sym.size

        print(sym)
        for insn in arch.disassemble(loPC, hiPC - 1):
            print("  0x%016x: %s" % ( insn['addr'], insn['asm'] ));


ds = __DisassembleSymbol('ds', gdb.COMMAND_DATA)
