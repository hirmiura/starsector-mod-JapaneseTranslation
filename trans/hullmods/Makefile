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
.PHONY: setup generate-pot merge-po
setup: ## セットアップ - ビルドの前準備
setup: check generate-pot merge-po

F_HMC		:= hull_mods.csv
F_HMC_POT	:= $(F_HMC).pot
F_HMC_PO	:= $(F_HMC).po
F_HMC_MO	:= $(F_HMC).mo

generate-pot: $(F_HMC_POT)

$(F_HMC_POT): $(D_SSDATA)/hullmods/$(F_HMC)
	@echo -e '$(CC_BrBlue)========== $(F_HMC_POT) ==========$(CC_Reset)'
	$(D_BIN)/hullmod2pot.py -d . $<

merge-po: $(F_HMC_PO)

$(F_HMC_PO): $(F_HMC_POT)
	@echo -e '$(CC_BrBlue)========== $(F_HMC_PO) ==========$(CC_Reset)'
	if [[ -f "$(F_HMC_PO)" ]] ; then \
		msgmerge --lang=ja --backup=t -U $@ $< ; \
	else \
		cp -f $< $@ ; \
	fi


#==============================================================================
# ビルド
#==============================================================================
.PHONY: build generate-mo translate
build: ## ビルドする
build: setup generate-mo translate

generate-mo: $(F_HMC_MO)

$(F_HMC_MO): $(F_HMC_PO)
	@echo -e '$(CC_BrBlue)========== $(F_HMC_MO) ==========$(CC_Reset)'
	msgfmt --statistics -o $@ $^

translate: $(F_HMC)

$(F_HMC): $(F_HMC_MO) $(D_SSDATA)/hullmods/$(F_HMC)
	@echo -e '$(CC_BrBlue)========== $(F_HMC) ==========$(CC_Reset)'
	$(D_BIN)/mo2hullmod.py -t -m $(F_HMC_MO) -d . $(D_SSDATA)/hullmods/$(F_HMC)


#==============================================================================
# クリーンアップ
#==============================================================================
.PHONY: clean clean-all clean-pot clean-mo clean-csv clean-backup
clean: ## セットアップで生成したファイル以外を全て削除します
clean: clean-pot

clean-all: ## 生成した全てのファイルを削除します
clean-all: clean clean-mo clean-csv clean-backup

clean-pot:
	@echo -e '$(CC_BrMagenta)========== clean-pot ==========$(CC_Reset)'
	rm -f *.pot

clean-mo:
	@echo -e '$(CC_BrMagenta)========== clean-mo ==========$(CC_Reset)'
	rm -f *.mo

clean-csv:
	@echo -e '$(CC_BrMagenta)========== clean-csv ==========$(CC_Reset)'
	rm -f *.csv

clean-backup:
	@echo -e '$(CC_BrMagenta)========== clean-backup ==========$(CC_Reset)'
	rm -f *~
