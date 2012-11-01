# rules to be imported by VERSION/Makefile

.PHONY: clean check

all: $(MOS)

rewrap:
	for f in $$(git st --porcelain *.po | egrep ".M " | cut -c 8-); do \
		echo $$f; \
		msgcat --no-wrap $$f | sponge $$f; \
	done

ifdef UPDATE_FROM

update:
	for f in *.po; do \
		msgmerge --no-wrap -N ../${UPDATE_FROM}/$$f $$f | ../tools/nostale.py | sponge $$f; \
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
