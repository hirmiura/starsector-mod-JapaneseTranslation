# SPDX-License-Identifier: MIT
# Copyright 2023 hirmiura (https://github.com/hirmiura)
#
SHELL := /bin/bash

# このパッケージのバージョン
# V_VERSION := $(shell tomlq -r '.tool.poetry.version' pyproject.toml)

# 各種ディレクトリ
D_SSHOME	:= Starsector
D_SSDATA	:= $(D_SSHOME)/starsector-core/data
D_BIN		:= bin
D_TRANS		:= trans
D_TMP		:= tmp
D_MOD		:= mod
D_ID		:= $(shell jq -r '.id' $(D_MOD)/mod_info.json)


#==============================================================================
# カラーコード
# ヘルプ表示
#==============================================================================
include ColorCode.mk
include Help.mk


#==============================================================================
# Starsecto本体へのリンク/ディレクトリを確認
#==============================================================================
.PHONY: check
check: ## Starsecto本体へのリンク/ディレクトリを確認します
check:
	@echo -e '$(CC_BrBlue)========== check ==========$(CC_Reset)'
	@echo '"$(D_SSHOME)" をチェックしています'
	@if [[ -L $(D_SSHOME) && `readlink $(D_SSHOME) ` ]] ; then \
		echo -e '    $(CC_BrGreen)SUCCESS$(CC_Reset): リンクです' ; \
	elif [[ -d $(D_SSHOME) ]] ; then \
		echo -e '    $(CC_BrGreen)SUCCESS$(CC_Reset): ディレクトリです' ; \
	else \
		echo -e '    \a$(CC_BrRed)ERROR: "$(D_SSHOME)" に "Starsector" へのリンクを張って下さい$(CC_Reset)' ; \
		echo -e '    $(CC_BrRed)例: ln -s /mnt/c/Program\ Files\ \(x86\)/Fractal\ Softworks/Starsector$(CC_Reset)' ; \
		exit 1 ; \
	fi


#==============================================================================
# セットアップ
#==============================================================================
.PHONY: setup
setup: ## セットアップ - ビルドの前準備
setup: check
	@echo -e '$(CC_BrBlue)========== setup ==========$(CC_Reset)'
	$(MAKE) -C $(D_TRANS) setup


#==============================================================================
# ビルド
#==============================================================================
.PHONY: build
build: ## ビルドする
build: setup build-trans
	@echo -e '$(CC_BrBlue)========== build ==========$(CC_Reset)'
	$(MAKE) -C $(D_TRANS) build


#==============================================================================
# パッケージング
#==============================================================================
.PHONY: packaging
packaging: ## パッケージ化する
packaging: build clean-package $(D_ID).zip

$(D_ID).zip:
	@echo -e '$(CC_BrBlue)========== $(D_ID).zip ==========$(CC_Reset)'
	cp -r $(D_MOD) $(D_ID)
	zip -r $(D_ID).zip $(D_ID)
	rm -fr $(D_ID)


#==============================================================================
# 全ての作業を一括で実施する
#==============================================================================
.PHONY: all
all: ## 全ての作業を一括で実施する
all: setup build packaging


#==============================================================================
# クリーンアップ
#==============================================================================
.PHONY: clean clean-all clean-tmp clean-package
clean: ## セットアップで生成したファイル以外を全て削除します
clean: clean-package
	@echo -e '$(CC_BrMagenta)========== clean ==========$(CC_Reset)'
	$(MAKE) -C $(D_TRANS) clean


clean-all: ## 生成した全てのファイルを削除します
clean-all: clean clean-tmp
	@echo -e '$(CC_BrMagenta)========== clean-all ==========$(CC_Reset)'
	$(MAKE) -C $(D_TRANS) clean-all

clean-tmp:
	@echo -e '$(CC_BrMagenta)========== clean-tmp ==========$(CC_Reset)'
	rm -fr $(D_TMP)

clean-package:
	@echo -e '$(CC_BrMagenta)========== clean-package ==========$(CC_Reset)'
	rm -fr $(D_ID).zip $(D_ID)
