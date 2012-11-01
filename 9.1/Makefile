LANG = it
VERSION = 9.1
UPDATE_FROM = 9.2

POS = $(wildcard *.po)
MOS = $(patsubst %-$(LANG).po,%-$(VERSION).mo,$(POS))

include ../rules.mk
