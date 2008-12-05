
TESTS = \
	BBChopTest.test \
	entropiesTest.test \
	testdag.test \
	testDagRead.test


all: $(TESTS)
	echo "ALL PASSED"

topdir = $(shell (cd ../; pwd))
RUNPY=PYTHONPATH=$(topdir)/source/ python




%.test: %.py
	$(RUNPY) $<