SUBDIRS = 10.0 9.6 9.5 9.4 9.3 9.2

all dlpots updatepots check popack mopack clean notrivial pgtrpush:
	for dir in $(SUBDIRS); do $(MAKE) -C $$dir $@; done

update:
	$(MAKE) -C 9.6 update
	$(MAKE) -C 9.5 update
	$(MAKE) -C 9.4 update
	$(MAKE) -C 9.3 update
	$(MAKE) -C 9.2 update
