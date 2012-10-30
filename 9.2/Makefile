POS = $(wildcard *.po)
MOS = $(patsubst %.po,%.mo,$(POS))

.PHONY: clean

all: $(MOS)

rewrap:
	for f in $$(git st --porcelain *.po | egrep ".M " | cut -c 8-); do \
		echo $$f; \
		msgcat --no-wrap $$f | sponge $$f; \
	done


clean:
	rm -f $(MOS)

%.mo : %.po
		msgfmt -o $@ -v -c $<
