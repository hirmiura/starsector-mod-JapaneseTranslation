# Makefile @ /trans
STARSECTOR_COREDATA = $(STARSECTOR)/starsector-core/data/
TRANS_DIR := ./
ORIGINAL_SUFFIX := .orig
PYTHON = python
SRC_DIR := ../src/
MOD_DIR := ../mod/

.PHONY: install mo2csv copy-original init-pot

install: mo2csv
	mv hull_mods.csv $(MOD_DIR)data/hullmods/

mo2csv:
	msgfmt hull_mods.orig.csv.ja.po -o hull_mods.orig.csv.ja.mo
	$(PYTHON) $(SRC_DIR)mo2hullmod.py -t hull_mods.orig.csv.ja.mo

copy-original:
	cp "$(STARSECTOR_COREDATA)hullmods/hull_mods.csv" $(TRANS_DIR)hull_mods$(ORIGINAL_SUFFIX).csv

init-pot:
	$(PYTHON) $(SRC_DIR)hullmod2pot.py hull_mods$(ORIGINAL_SUFFIX).csv
