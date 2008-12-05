all: run_test run_etest

topdir = $(shell (cd ../; pwd))
RUNPY=PYTHONPATH=$(topdir)/source/ python

run_test:
	$(RUNPY) BBChopTest.py


run_etest:
	$(RUNPY) entropiesTest.py

run_dagtest:
	$(RUNPY) testdag.py
