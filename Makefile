# Makefile @ /
STARSECTOR_COREDATA = "$(STARSECTOR)/starsector-core/data/"
TRANS_DIR := trans/
ORIGINAL_SUFFIX := .orig
ZIP := zip
SRC_NAME := mod
DST_NAME := "Japanese Translation"
ZIP_NAME := Japanese_Translation.zip

.PHONY: all copy-original package clean clean-package clean-original

all: package

copy-original:
	cp $(STARSECTOR_COREDATA)hullmods/hull_mods.csv $(TRANS_DIR)hull_mods$(ORIGINAL_SUFFIX).csv

package:
	cp -r $(SRC_NAME) $(DST_NAME)
	cp $(TRANS_DIR)hull_mods.csv $(DST_NAME)/data/hullmods/
	cp CHANGELOG.md README.md $(DST_NAME)
	$(ZIP) -r $(ZIP_NAME) $(DST_NAME)

clean: clean-package

clean-package:
	rm -fr $(ZIP_NAME) $(DST_NAME)

clean-original:
	rm -f $(TRANS_DIR)*.orig $(TRANS_DIR)*.orig.*
