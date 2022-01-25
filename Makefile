# Makefile @ /
STARSECTOR_COREDATA = "$(STARSECTOR)/starsector-core/data/"
ORIGINAL_SUFFIX := .orig
ZIP := zip
MOD_DIR := mod/
DST_NAME := "Japanese Translation"
ZIP_NAME := Japanese_Translation.zip

.PHONY: all copy-original package clean clean-package clean-original

all: package

package:
	make -C trans install
	cp -r $(MOD_DIR) $(DST_NAME)
	cp CHANGELOG.md README.md $(DST_NAME)
	$(ZIP) -r $(ZIP_NAME) $(DST_NAME)

clean: clean-package

clean-package:
	rm -fr $(ZIP_NAME) $(DST_NAME)
