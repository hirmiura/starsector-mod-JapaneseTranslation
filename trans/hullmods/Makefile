# SPDX-License-Identifier: MIT
# Copyright 2023 hirmiura (https://github.com/hirmiura)
#
SHELL := /bin/bash

# 各種ディレクトリ
D_SSHOME	:= ../../Starsector
D_SSDATA	:= $(D_SSHOME)/starsector-core/data
D_BIN		:= ../../bin
D_TRANS		:= ../../trans
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
setup: check

generate-pot:
	$(D_BIN)/hullmod2pot.py hull_mods$(ORIGINAL_SUFFIX).csv


#==============================================================================
# ビルド
#==============================================================================
.PHONY: build build-trans
build: ## ビルドする
build: setup build-trans

build-trans:
	@echo -e '$(CC_BrBlue)========== build-trans ==========$(CC_Reset)'
	$(MAKE) -C $(D_TRANS) install

