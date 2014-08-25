SUBDIRS = 9.4 9.3 9.2 9.1 9.0 8.4

all dlpots updatepots check popack mopack clean notrivial pgtrpush:
	for dir in $(SUBDIRS); do $(MAKE) -C $$dir $@; done

update:
	$(MAKE) -C 9.3 update
	$(MAKE) -C 9.2 update
	$(MAKE) -C 9.1 update
	$(MAKE) -C 9.0 update
	$(MAKE) -C 8.4 update
