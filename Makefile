# Makefile @ /
ZIP = zip
DIR_NAME = "Japanese Translation"
ZIP_NAME = Japanese_Translation.zip

.PHONY: all compress clean

all: compress

compress: clean
	$(ZIP) -r $(ZIP_NAME) $(DIR_NAME)

clean:
	rm -f $(ZIP_NAME)
