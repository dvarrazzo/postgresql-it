LANG = it
VERSION = 9.3
PGTR_BRANCH=master

POS = $(wildcard *.po)
MOS = $(patsubst %.po,%-$(VERSION).mo,$(POS))
URLPATTERN ?= "po-current"

include ../rules.mk
