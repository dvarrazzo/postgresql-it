LANG = it
VERSION = 9.3

POS = $(wildcard *.po)
MOS = $(patsubst %.po,%-$(VERSION).mo,$(POS))
URLPATTERN ?= "po-$(VERSION)"

include ../rules.mk
