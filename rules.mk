# rules to be imported by VERSION/Makefile

ROOT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

.PHONY: clean check

all: $(MOS)

URLPATTERN ?= "po-$(VERSION)-branch"

# download .pot files from PG website
dlpots:
	for u in $$(wget -O - http://babel.postgresql.org/ \
			| egrep  "href=\"$(URLPATTERN)/.*pot\"" \
			| sed -e 's/.*href="\(.*\)".*/\1/'); do \
		wget -O $$(basename $$u) http://babel.postgresql.org/$$u; \
	done

# update .po files with the new strings downloaded by dlpots
updatepots:
	for f in *.po; do \
		msgmerge -N $$f $${f%.po}.pot | ../tools/nostale.py | sponge $$f; \
		../tools/notrivial $$f; \
	done

ifdef UPDATE_FROM

# copy translations from newer PG version to this
update:
	for f in *.po; do \
		msgmerge -N ../${UPDATE_FROM}/$$f $$f | ../tools/nostale.py | sponge $$f; \
		sed -i 's/\(Project-Id-Version:.* \)\(${UPDATE_FROM}\)\(.*\)/\1${VERSION}\3/' $$f; \
		../tools/notrivial $$f; \
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

# Revert files whose only changes are in comments and metadata
notrivial:
	../tools/notrivial *.po

# Look for translation errors
check: $(MOS)
	../tools/chkpos.py $(POS)

clean:
	rm -f *.mo *.pot

# NOTE: this doesn't generate all the expected file names:
# ecpglib -> ecpglib6
# libpq -> libpq5
%-$(VERSION).mo : %.po
		msgfmt -o $@ -v -c $<

popack:
	tar cjvf ../package/postgresql-$(LANG)-$(VERSION).tar.bz2 *.po

mopack:
	mkdir -p ../package
	make clean
	make
	mv libpq-$(VERSION).mo libpq5-$(VERSION).mo
	-mv ecpglib-$(VERSION).mo ecpglib6-$(VERSION).mo
	zip -9 ../package/messages-$(LANG)-$(VERSION).zip *.mo

# propagate the changes to a pgtranslation working copy
# you need a symlink called 'pgtr' in the current directory,
# pointing to the pgtranslation messages repository
pgtrpush:
	(cd ../pgtr && git checkout $(PGTR_BRANCH) && git pull)
	for f in *.po; do \
		msgcat --no-wrap -o ../pgtr/$(LANG)/$$f $$f; \
	done
	(cd ../pgtr && $(ROOT_DIR)/tools/notrivial $(LANG)/*.po)
	(cd ../pgtr && git status --porcelain | grep -q '^ M' && git commit -m "$(LANG): translation updates" $(LANG) || true)
