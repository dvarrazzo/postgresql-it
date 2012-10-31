# rules to be imported by VERSION/Makefile

.PHONY: clean check

all: $(MOS)

rewrap:
	for f in $$(git st --porcelain *.po | egrep ".M " | cut -c 8-); do \
		echo $$f; \
		msgcat --no-wrap $$f | sponge $$f; \
	done

check:
	../tools/chkpos.py $(POS)

clean:
	rm -f $(MOS)

# NOTE: this doesn't generate all the expected file names:
# ecpglib -> ecpglib6
# libpq -> libpq5
%-$(VERSION).mo : %-$(LANG).po
		msgfmt -o $@ -v -c $<
