# SPDX-License-Identifier: MIT
# Copyright 2023 hirmiura (https://github.com/hirmiura)
#
SHELL := /bin/bash

# 各種ディレクトリ
D_BIN		:= ../../../bin
D_MODDST	:= ../../../mod/data/world/factions
D_SSCMP		:= ../../../Starsector/starsector-core/data/world/factions


#==============================================================================
# カラーコード
# ヘルプ表示
#==============================================================================
include ../../../ColorCode.mk
include ../../../Help.mk


#==============================================================================
# Starsecto本体へのリンク/ディレクトリを確認
#==============================================================================
.PHONY: check
check: ## Starsecto本体へのリンク/ディレクトリを確認します
check:
	@echo -e '$(CC_BrBlue)========== $@ ==========$(CC_Reset)'
	$(MAKE) -C ../../.. check


#==============================================================================
# セットアップ
#==============================================================================
.PHONY: setup generate-pot merge-po
setup: ## セットアップ - ビルドの前準備
setup: check generate-pot merge-po

generate-pot: default_ranks.pot

default_ranks.pot: default_ranks.toml $(D_SSCMP)/default_ranks.json
	@echo -e '$(CC_BrBlue)========== $@ ==========$(CC_Reset)'
	$(D_BIN)/json2pot.py -c $<

merge-po: default_ranks.edit.po default_ranks.po

default_ranks.edit.po:: default_ranks.pot
	@echo -e '$(CC_BrBlue)========== $@ ==========$(CC_Reset)'
	if [[ -f "$@" ]] ; then \
		msgmerge --lang=ja --no-fuzzy-matching --backup=t -U $@ $< ; \
	else \
		msginit --no-translator -l ja_JP.utf8 -i $< -o $@ ; \
	fi

default_ranks.edit.po::
	@echo -e '$(CC_BrBlue)========== $@ ==========$(CC_Reset)'
	$(eval FN := default_ranks.po)
	if [[ -f "$(FN)" ]] ; then \
		msgcat --use-first -o $@ $@ $(FN); \
	fi \

default_ranks.po: default_ranks.edit.po
	@echo -e '$(CC_BrBlue)========== $@ ==========$(CC_Reset)'
	if [[ -f "$@" ]] ; then \
		msgcat --use-first --no-location --no-wrap --sort-output -o $@ $< $@ ; \
	else \
		msgcat --no-location --no-wrap --sort-output -o $@ $< ; \
	fi
	msgattrib --no-obsolete --no-location --no-wrap --sort-output -o - $@ \
	| grep -vE '^"(POT-Creation-Date|X-Generator):.*\\n"' \
	| sponge $@
	# msgcat --no-location --no-wrap --sort-output $@ \


#==============================================================================
# ビルド
#==============================================================================
.PHONY: build generate-mo translate
build: ## ビルドする
build: setup generate-mo translate copy-json

generate-mo: default_ranks.mo

default_ranks.mo: default_ranks.po
	@echo -e '$(CC_BrBlue)========== $@ ==========$(CC_Reset)'
	msgfmt --statistics -o $@ $^

translate: default_ranks.json

default_ranks.json: default_ranks.mo default_ranks.toml $(D_SSCMP)/default_ranks.json
	@echo -e '$(CC_BrBlue)========== $@ ==========$(CC_Reset)'
	$(D_BIN)/mo2json.py -m $< -c default_ranks.toml

copy-json: default_ranks.json
	@echo -e '$(CC_BrBlue)========== $@ ==========$(CC_Reset)'
	@mkdir -p $(D_MODDST)
	cp $< $(D_MODDST)


#==============================================================================
# クリーンアップ
#==============================================================================
.PHONY: clean clean-all clean-pot clean-mo clean-json clean-backup clean-package
clean: ## セットアップで生成したファイル以外を全て削除します
clean: clean-mo clean-json clean-package

clean-all: ## 生成した全てのファイルを削除します
clean-all: clean clean-pot clean-backup

clean-pot:
	@echo -e '$(CC_BrMagenta)========== $@ ==========$(CC_Reset)'
	rm -f *.pot

clean-mo:
	@echo -e '$(CC_BrMagenta)========== $@ ==========$(CC_Reset)'
	rm -f *.mo

clean-json:
	@echo -e '$(CC_BrMagenta)========== $@ ==========$(CC_Reset)'
	rm -f *.json

clean-backup:
	@echo -e '$(CC_BrMagenta)========== $@ ==========$(CC_Reset)'
	rm -f *~

clean-package:
	@echo -e '$(CC_BrMagenta)========== $@ ==========$(CC_Reset)'
	rm -fr $(D_MODDST)
