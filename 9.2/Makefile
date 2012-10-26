POS = $(wildcard *.po)
MOS = $(patsubst %.po,%.mo,$(POS))

.PHONY: clean

all: $(MOS)

clean:
	rm -f $(MOS)

%.mo : %.po
		msgfmt -o $@ -v -c $<
