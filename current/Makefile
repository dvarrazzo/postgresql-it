LANG = it
VERSION = current

POS = $(wildcard *.po)
MOS = $(patsubst %.po,%-$(VERSION).mo,$(POS))
URLPATTERN ?= "po-$(VERSION)"

include ../rules.mk
