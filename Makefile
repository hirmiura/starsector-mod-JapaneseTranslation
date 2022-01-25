# Makefile @ /
ZIP = zip
SRC_NAME = mod
DST_NAME = "Japanese Translation"
ZIP_NAME = Japanese_Translation.zip

.PHONY: all package clean

all: package

package:
	cp -r $(SRC_NAME) $(DST_NAME)
	cp CHANGELOG.md LICENSE.md README.md $(DST_NAME)
	$(ZIP) -r $(ZIP_NAME) $(DST_NAME)

clean:
	rm -fr $(ZIP_NAME) $(SRC_NAME)
