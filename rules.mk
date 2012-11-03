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

# Copy the translations from the longer files to the shortest files, to make
# sure the same message translated the same way.
uniform:
	for i in $$(seq $$(ls -1 *.po | wc -l)); do \
		for j in $$(seq $$(($$i + 1)) $$(ls -1 *.po | wc -l)); do \
			msgmerge -N $$(ls -1S *.po | head -n $$i | tail -n 1) \
					$$(ls -1S *.po | head -n $$j | tail -n 1) \
				| ../tools/nostale.py \
				| sponge $$(ls -1S *.po | head -n $$j | tail -n 1); \
		done \
	done

check: $(MOS)
	../tools/chkpos.py $(POS)

clean:
	rm -f *.mo

# NOTE: this doesn't generate all the expected file names:
# ecpglib -> ecpglib6
# libpq -> libpq5
%-$(VERSION).mo : %-$(LANG).po
		msgfmt -o $@ -v -c $<

package:
	mkdir -p ../package
	make clean
	make
	mv libpq-$(VERSION).mo libpq5-$(VERSION).mo
	mv ecpglib-$(VERSION).mo ecpglib6-$(VERSION).mo
	zip -9 ../package/messages-$(LANG)-$(VERSION).zip *.mo
