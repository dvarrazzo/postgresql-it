LANG = it
VERSION = 9.2

POS = $(wildcard *.po)
MOS = $(patsubst %-$(LANG).po,%-$(VERSION).mo,$(POS))

.PHONY: clean

all: $(MOS)

rewrap:
	for f in $$(git st --porcelain *.po | egrep ".M " | cut -c 8-); do \
		echo $$f; \
		msgcat --no-wrap $$f | sponge $$f; \
	done

clean:
	rm -f $(MOS)

# NOTE: this doesn't generate all the expected file names:
# ecpglib -> ecpglib6
# libpq -> libpq5
%-$(VERSION).mo : %-$(LANG).po
		msgfmt -o $@ -v -c $<
