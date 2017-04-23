LANG = it
VERSION = 10.0
PGTR_BRANCH = master
URLPATTERN = "po-master"

POS = $(wildcard *.po)
MOS = $(patsubst %.po,%-$(VERSION).mo,$(POS))

include ../rules.mk
