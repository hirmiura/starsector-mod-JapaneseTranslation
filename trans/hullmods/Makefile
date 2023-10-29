# SPDX-License-Identifier: MIT
# Copyright 2023 hirmiura (https://github.com/hirmiura)
#
SHELL := /bin/bash

# 各種ディレクトリ
D_BIN		:= ../../bin
D_MOD		:= ../../mod
D_DHM		:= data/hullmods
D_MODDST	:= $(D_MOD)/$(D_DHM)
D_SSHOME	:= ../../Starsector
D_SSDHM		:= $(D_SSHOME)/starsector-core/$(D_DHM)

# 各種ファイル名
F_HMC		:= hull_mods.csv
F_HMC_POT	:= $(F_HMC).pot
F_HMC_PO	:= $(F_HMC).po
F_HMC_MO	:= $(F_HMC).mo


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
	@echo -e '$(CC_BrBlue)========== check ==========$(CC_Reset)'
	$(MAKE) -C ../.. check


#==============================================================================
# セットアップ
#==============================================================================
.PHONY: setup generate-pot merge-po
setup: ## セットアップ - ビルドの前準備
setup: check generate-pot merge-po

generate-pot: $(F_HMC_POT)

$(F_HMC_POT): $(D_SSDHM)/$(F_HMC)
	@echo -e '$(CC_BrBlue)========== $(F_HMC_POT) ==========$(CC_Reset)'
	$(D_BIN)/hullmod2pot.py -d . $<

merge-po: $(F_HMC_PO)

$(F_HMC_PO): $(F_HMC_POT)
	@echo -e '$(CC_BrBlue)========== $(F_HMC_PO) ==========$(CC_Reset)'
	if [[ -f "$(F_HMC_PO)" ]] ; then \
		msgmerge --lang=ja --no-fuzzy-matching --backup=t -U $@ $< ; \
	else \
		cp -f $< $@ ; \
	fi


#==============================================================================
# ビルド
#==============================================================================
.PHONY: build generate-mo translate
build: ## ビルドする
build: setup generate-mo translate copy-csv

generate-mo: $(F_HMC_MO)

$(F_HMC_MO): $(F_HMC_PO)
	@echo -e '$(CC_BrBlue)========== $(F_HMC_MO) ==========$(CC_Reset)'
	msgfmt --statistics -o $@ $^

translate: $(F_HMC)

$(F_HMC): $(F_HMC_MO) $(D_SSDHM)/$(F_HMC)
	@echo -e '$(CC_BrBlue)========== $(F_HMC) ==========$(CC_Reset)'
	$(D_BIN)/mo2hullmod.py -t -m $(F_HMC_MO) -d . $(D_SSDHM)/$(F_HMC)

copy-csv: $(F_HMC)
	@echo -e '$(CC_BrBlue)========== copy-csv ==========$(CC_Reset)'
	@mkdir -p $(D_MODDST)
	cp $(F_HMC) $(D_MODDST)


#==============================================================================
# クリーンアップ
#==============================================================================
.PHONY: clean clean-all clean-pot clean-mo clean-csv clean-backup clean-package
clean: ## セットアップで生成したファイル以外を全て削除します
clean: clean-mo clean-csv clean-package

clean-all: ## 生成した全てのファイルを削除します
clean-all: clean clean-pot clean-backup

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

clean-package:
	@echo -e '$(CC_BrMagenta)========== clean-package ==========$(CC_Reset)'
	rm -f $(D_MODDST)/*
