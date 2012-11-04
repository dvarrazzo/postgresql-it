SUBDIRS = 9.2 9.1 9.0 8.4 8.3

.PHONY: all update check clean

all:
	for dir in $(SUBDIRS); do $(MAKE) -C $$dir all; done

dlpots:
	for dir in $(SUBDIRS); do $(MAKE) -C $$dir dlpots; done

updatepots:
	for dir in $(SUBDIRS); do $(MAKE) -C $$dir updatepots; done

update:
	$(MAKE) -C 9.1 update
	$(MAKE) -C 9.0 update
	$(MAKE) -C 8.4 update
	$(MAKE) -C 8.3 update

check:
	for dir in $(SUBDIRS); do $(MAKE) -C $$dir check; done

popack:
	for dir in $(SUBDIRS); do $(MAKE) -C $$dir popack; done

mopack:
	for dir in $(SUBDIRS); do $(MAKE) -C $$dir mopack; done

clean:
	for dir in $(SUBDIRS); do $(MAKE) -C $$dir clean; done
