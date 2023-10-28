# SPDX-License-Identifier: MIT
# Copyright 2023 hirmiura (https://github.com/hirmiura)
#
SHELL := /bin/bash

# 各種ディレクトリ
D_SSHOME	:= ../../Starsector
D_SSDATA	:= $(D_SSHOME)/starsector-core/data
D_BIN		:= ../../bin
D_TRANS		:= ../../trans
D_OLDTRANS	:= ../../oldtrans
D_TMP		:= ../../tmp
D_MOD		:= ../../mod


#==============================================================================
# カラーコード
#==============================================================================
include ../../ColorCode.mk


#==============================================================================
# ヘルプ表示
#==============================================================================
define find.functions
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'
endef

.PHONY: help
help:
	@echo '以下のコマンドが使用できます'
	@echo ''
	$(call find.functions)


#==============================================================================
# Starsecto本体へのリンク/ディレクトリを確認
#==============================================================================
.PHONY: check
check: ## Starsecto本体へのリンク/ディレクトリを確認します
check:
	@echo -e '$(CC_BrBlue)========== check ==========$(CC_Reset)'
	$(MAKE) -C ../.. check


#==============================================================================
# セットアップ
#==============================================================================
.PHONY: setup
setup: ## セットアップ - ビルドの前準備
setup: check generate-pot

F_HMC_POT	:= hull_mods.csv.pot
F_HMC_JPO	:= hull_mods.csv.ja.po

generate-pot: $(F_HMC_POT)

$(F_HMC_POT): $(D_SSDATA)/hullmods/hull_mods.csv
	@echo -e '$(CC_BrBlue)========== $(F_HMC_POT) ==========$(CC_Reset)'
	$(D_BIN)/hullmod2pot.py -d . $(D_SSDATA)/hullmods/hull_mods.csv

merge-po: $(F_HMC_JPO)

$(F_HMC_JPO): $(F_HMC_POT)
	@echo -e '$(CC_BrBlue)========== $(F_HMC_JPO) ==========$(CC_Reset)'
	if [[ -f "$(F_HMC_JPO)" ]] ; then \
		msgmerge --lang=ja --backup=t -U $@ $< ; \
	fi


#==============================================================================
# ビルド
#==============================================================================
.PHONY: build build-trans
build: ## ビルドする
build: setup build-trans

build-trans:
	@echo -e '$(CC_BrBlue)========== build-trans ==========$(CC_Reset)'


#==============================================================================
# クリーンアップ
#==============================================================================
.PHONY: clean clean-all clean-pot
clean: ## セットアップで生成したファイル以外を全て削除します
clean: clean-pot

clean-all: ## 生成した全てのファイルを削除します
clean-all: clean clean-mo

clean-pot:
	@echo -e '$(CC_BrMagenta)========== clean-pot ==========$(CC_Reset)'
	rm -fr *.pot

clean-mo:
	@echo -e '$(CC_BrMagenta)========== clean-mo ==========$(CC_Reset)'
	rm -fr *.mo
