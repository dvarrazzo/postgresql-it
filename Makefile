SUBDIRS = 8.4 9.0 9.1 9.2

.PHONY: all update check clean

all:
	for dir in $(SUBDIRS); do $(MAKE) -C $$dir all; done

update:
	$(MAKE) -C 9.1 update
	$(MAKE) -C 9.0 update
	$(MAKE) -C 8.4 update

check:
	for dir in $(SUBDIRS); do $(MAKE) -C $$dir check; done

clean:
	for dir in $(SUBDIRS); do $(MAKE) -C $$dir clean; done

