# Builds using the default cpp toolchain for current arch (if you
# want to cross compile you'll need to call cmake manually)

HOST   := $(shell uname -m)-$(shell uname -s | tr A-Z a-z)
TARGET ?= $(HOST)
BUILD  ?= build/$(TARGET)
LAUNCHER ?= $(BUILD)/lmr
CONFIG ?= Debug

BASEADDR= 16r1FF10000

all: $(LAUNCHER) $(LAUNCHER)-gdb.py
	@echo
	@echo "Build output is in"
	@echo "    $(BUILD)"
	@echo

$(LAUNCHER): $(BUILD) *.cpp *.h
	cmake --build $(BUILD) --config $(CONFIG)

$(LAUNCHER)-gdb.py: debug/powerlang-gdb.py.in
	sed "s#@POWERLANG_GDB_PYDIR@#$(shell realpath $(shell dirname $<))#g" $< > $@

$(BUILD): CMakeLists.txt
	cmake -B $(BUILD)

clean:
	rm -rf $(BUILD)
