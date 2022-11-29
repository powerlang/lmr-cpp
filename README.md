# C++ LMR launcher

This repo groups the tools needed to launch and debug native LMR-based Smalltalks. 
The launcher is able to read native image segments, the `debug` dir contains a set
of python/gdb scripts to allow inspecting the LMR memory.

# Building

To build for your currently running system, just run `make`.

This compiles launcher executable (`bee-dmr`). You will need a kernel image (`bee-dmr.bsl`) in
`build/<arch>-<os>` (so if you're running Linux on x86_64, it's `build/x86_64-linux`).
You'll have to generate that manually (we will add a target to the makefile eventually).

# Building launcher for Windows

For windows from linux (using mingw64) do:

```
cd launcher
$ cmake -B build -DCMAKE_TOOLCHAIN_FILE=toolchain-mingw64.cmake
cd build
make
```

For Windows from Windows, you will need a C++ compiler. Instructions here are for
mingw-64 (clang should also be possible). To install mingw64, follow the instructions
[here](https://code.visualstudio.com/docs/cpp/config-mingw). Make sure to install it
in a path without spaces (like C:/mingw-w64) or you may face errors. Add it to path,
in my case it was `C:\mingw-w64\x86_64-8.1.0-posix-seh-rt_v6-rev0\mingw64\bin`.
Install CMake and be sure to have its path added too. Then do:

```
cd launcher
$ cmake -B build -G "MinGW Makefiles"
cd build
make
```

# Running

Assuming you have built everything as descibed above, you may run it by:

```
cd build/x86_64-linux # or other <arch>-<os> directory
./bee-dmr bee-dmr.bsl
echo $?
```
This last should echo "3" as the result of the computation.

This is because the code executed is something like
```smalltalk
"bee-dmr/Kernel/Kernel.st"
Kernel >> entry: argc argv: argv [
	<callback: long (long, pointer)>
	"^Smalltalk startSession"
	^Kernel new foo.
]

Kernel >> foo [
	| result |
	result := 42 factorial.
	^result = 0x3C1581D491B28F523C23ABDF35B689C908000000000 
		ifTrue: [1] 
		ifFalse: [0]
]
```
So the unboxed encoding of "1" is returned.

The encoding for smallIntegers is ((smallInt bitShift: 1) + 1), so (1 bitShift: 1) + 1 -> 3.


