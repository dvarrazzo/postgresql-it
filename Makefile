SUBDIRS = 9.1 9.2

.PHONY: all update rewrap check clean

all:
	for dir in $(SUBDIRS); do $(MAKE) -C $$dir all; done

update:
	$(MAKE) -C 9.1 update

rewrap:
	for dir in $(SUBDIRS); do $(MAKE) -C $$dir rewrap; done

check:
	for dir in $(SUBDIRS); do $(MAKE) -C $$dir check; done

clean:
	for dir in $(SUBDIRS); do $(MAKE) -C $$dir clean; done

