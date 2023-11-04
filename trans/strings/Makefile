# SPDX-License-Identifier: MIT
# Copyright 2023 hirmiura (https://github.com/hirmiura)
#
SHELL := /bin/bash

# 各種ディレクトリ
D_BIN		:= ../../bin
D_SUBPATH	:= data/strings
D_MOD		:= ../../mod/$(D_SUBPATH)
D_SS		:= ../../Starsector/starsector-core/$(D_SUBPATH)


#==============================================================================
# カラーコード
# ヘルプ表示
#==============================================================================
include ../../ColorCode.mk
include ../../Help.mk


#==============================================================================
# Starsecto本体へのリンク/ディレクトリを確認
#==============================================================================
.PHONY: check
check: ## Starsecto本体へのリンク/ディレクトリを確認します
check:
	@echo -e '$(CC_BrBlue)========== $@ ==========$(CC_Reset)'
	$(MAKE) -C ../.. check


#==============================================================================
# セットアップ
#==============================================================================
.PHONY: setup generate-pot merge-po
setup: ## セットアップ - ビルドの前準備
setup: check generate-pot merge-po

generate-pot: strings.pot

%.pot: %.toml $(D_SS)/%.json
	@echo -e '$(CC_BrBlue)========== $@ ==========$(CC_Reset)'
	$(D_BIN)/json2pot.py -c $<

merge-po: strings.edit.po strings.po

%.edit.po:: %.pot
	@echo -e '$(CC_BrBlue)========== $@ ==========$(CC_Reset)'
	if [[ -f "$@" ]] ; then \
		msgmerge --lang=ja --no-fuzzy-matching --backup=t -U $@ $< ; \
	else \
		msginit --no-translator -l ja_JP.utf8 -i $< -o $@ ; \
	fi

%.edit.po::
	@echo -e '$(CC_BrBlue)========== $@ ==========$(CC_Reset)'
	$(eval FN := $(@:%.edit.po=%.po))
	if [[ -f "$(FN)" ]] ; then \
		msgcat --use-first -o $@ $@ $(FN); \
	fi \

%.po: %.edit.po
	@echo -e '$(CC_BrBlue)========== $@ ==========$(CC_Reset)'
	if [[ "$(suffix $(@:%.po=%))" != ".edit" ]] ; then \
		if [[ -f "$@" ]] ; then \
			msgcat --use-first --no-location --no-wrap --sort-output -o $@ $< $@ ; \
		else \
			msgcat --no-location --no-wrap --sort-output -o $@ $< ; \
		fi ; \
		msgattrib --no-obsolete --no-location --no-wrap --sort-output -o - $@ \
		| grep -vE '^"(POT-Creation-Date|X-Generator):.*\\n"' \
		| sponge $@ ; \
	fi


#==============================================================================
# ビルド
#==============================================================================
.PHONY: build generate-mo translate
build: ## ビルドする
build: setup generate-mo translate copy-json

generate-mo: strings.mo

%.mo: %.po
	@echo -e '$(CC_BrBlue)========== $@ ==========$(CC_Reset)'
	msgfmt --statistics -o $@ $^

translate: strings.json

%.json: %.mo %.toml $(D_SS)/%.json
	@echo -e '$(CC_BrBlue)========== $@ ==========$(CC_Reset)'
	$(D_BIN)/mo2json.py -m $< -c $(@:%.json=%.toml)

copy-json: strings.json
	@echo -e '$(CC_BrBlue)========== $@ ==========$(CC_Reset)'
	@mkdir -p $(D_MOD)
	cp $< $(D_MOD)


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
	rm -fr $(D_MOD)
