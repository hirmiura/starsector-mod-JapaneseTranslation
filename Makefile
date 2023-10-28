# Makefile @ /
STARSECTOR_COREDATA = "$(STARSECTOR)/starsector-core/data/"
ORIGINAL_SUFFIX := .orig
ZIP := zip
MOD_DIR := mod/
DST_NAME := JapaneseTranslation
ZIP_NAME := JapaneseTranslation.zip

.PHONY: all trans package clean clean-package

all: package

trans:
	make -C trans install

package: trans
	cp -r $(MOD_DIR) $(DST_NAME)
	cp CHANGELOG.md README.md $(DST_NAME)
	$(ZIP) -r $(ZIP_NAME) $(DST_NAME)

clean: clean-package

clean-package:
	rm -fr $(ZIP_NAME) $(DST_NAME)
