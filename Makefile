# SPDX-License-Identifier: MIT
# Copyright 2023 hirmiura (https://github.com/hirmiura)
#
SHELL := /bin/bash

# 各種ディレクトリ
D_SSHOME	:= Starsector
D_TRANS		:= trans
D_MOD		:= mod
F_MODINFO	:= $(D_MOD)/mod_info.json

# このパッケージのバージョン
V_ID		:= $(shell jq -r '.id' $(F_MODINFO))
V_VERSION	:= $(shell jq -r '.version' $(F_MODINFO))
F_PACKAGE	:= $(V_ID)-$(V_VERSION)


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
	@echo -e '$(CC_BrBlue)========== $@ ==========$(CC_Reset)'
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
	@echo -e '$(CC_BrBlue)========== $@ ==========$(CC_Reset)'
	$(MAKE) -C $(D_TRANS) setup


#==============================================================================
# ビルド
#==============================================================================
.PHONY: build
build: ## ビルドする
build: setup
	@echo -e '$(CC_BrBlue)========== $@ ==========$(CC_Reset)'
	$(MAKE) -C $(D_TRANS) build


#==============================================================================
# パッケージング
#==============================================================================
.PHONY: packaging
packaging: ## パッケージ化する
packaging: build clean-package $(F_PACKAGE).zip

$(F_PACKAGE).zip:
	@echo -e '$(CC_BrBlue)========== $@ ==========$(CC_Reset)'
	cp -r $(D_MOD) $(V_ID)
	zip -r $(F_PACKAGE).zip $(V_ID)
	rm -fr $(V_ID)


#==============================================================================
# 全ての作業を一括で実施する
#==============================================================================
.PHONY: all
all: ## 全ての作業を一括で実施する
all: setup build packaging


#==============================================================================
# クリーンアップ
#==============================================================================
.PHONY: clean clean-all clean-package
clean: ## セットアップで生成したファイル以外を全て削除します
clean: clean-package
	@echo -e '$(CC_BrMagenta)========== $@ ==========$(CC_Reset)'
	$(MAKE) -C $(D_TRANS) clean

clean-all: ## 生成した全てのファイルを削除します
clean-all: clean
	@echo -e '$(CC_BrMagenta)========== $@ ==========$(CC_Reset)'
	$(MAKE) -C $(D_TRANS) clean-all

clean-package:
	@echo -e '$(CC_BrMagenta)========== $@ ==========$(CC_Reset)'
	rm -fr $(F_PACKAGE).zip $(V_ID)
