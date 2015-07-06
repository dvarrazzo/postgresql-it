LANG = it
VERSION = 9.5
PGTR_BRANCH=master
URLPATTERN = "po-current"

POS = $(wildcard *.po)
MOS = $(patsubst %.po,%-$(VERSION).mo,$(POS))

include ../rules.mk
