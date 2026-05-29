UTILS_DIR=../utils
WAVE_DIR=./vcd
CIRCUIT=sub-impl.circ
SPEC=sub-spec.circ
TESTBENCH=sub-tb.circ
VCDVIEWER=gtkwave
WAVEFILE=$(WAVE_DIR)/sub.vcd
SPECFILE=$(WAVE_DIR)/spec.sim
GTKWFILE=$(WAVE_DIR)/sub.gtkw

SIGSPEC=a 1 b 1 c 1 cout 1 d 1

.PHONY: all clean view

default all: $(WAVE_DIR) view

$(WAVE_DIR):
	mkdir -p $(WAVE_DIR)

view: $(WAVEFILE)
	$(VCDVIEWER) $(GTKWFILE)

clean:
	rm -rf $(WAVEFILE) $(GTKWFILE) $(SPECFILE)

$(SPECFILE): $(SPEC) $(CIRCUIT) $(TESTBENCH)
	logisim -tty table $(TESTBENCH) -sub $(CIRCUIT) $(SPEC) > $@

$(WAVEFILE): $(SPECFILE) $(CIRCUIT) $(TESTBENCH) $(SPEC)
	logisim -tty table $(TESTBENCH) | $(UTILS_DIR)/logisim2vcd.py $@ -spec $(SPECFILE) $(SIGSPEC)
