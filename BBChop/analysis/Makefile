all: run_time

topdir = $(shell (cd ../; pwd))
RUNPY=PYTHONPATH=$(topdir)/source/ python

run_time:
	$(RUNPY) BBChopTime.py

