# rules to be imported by VERSION/Makefile

.PHONY: clean check

all: $(MOS)

ifdef UPDATE_FROM

update:
	for f in *.po; do \
		msgmerge -N ../${UPDATE_FROM}/$$f $$f | ../tools/nostale.py | sponge $$f; \
		sed -i 's/\(Project-Id-Version:.* \)\(${UPDATE_FROM}\)\(.*\)/\1${VERSION}\3/' $$f; \
	done

endif

check: $(MOS)
	../tools/chkpos.py $(POS)

clean:
	rm -f *.mo

# NOTE: this doesn't generate all the expected file names:
# ecpglib -> ecpglib6
# libpq -> libpq5
%-$(VERSION).mo : %-$(LANG).po
		msgfmt -o $@ -v -c $<
