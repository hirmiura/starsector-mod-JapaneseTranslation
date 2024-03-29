# SPDX-License-Identifier: MIT
# Copyright 2023 hirmiura (https://github.com/hirmiura)
#
#==============================================================================
# 翻訳ディレクトリ共通Makefile
#==============================================================================


#==============================================================================
# カラーコード
# ヘルプ表示
#==============================================================================
include $(D_REL)/ColorCode.mk
include $(D_REL)/Help.mk


#==============================================================================
# Starsecto本体へのリンク/ディレクトリを確認
#==============================================================================
.PHONY: check
check: ## Starsecto本体へのリンク/ディレクトリを確認します
check:
	@echo -e '$(CC_BrBlue)========== $@ ==========$(CC_Reset)'
	$(MAKE) -C $(D_REL) check


#==============================================================================
# セットアップ
#==============================================================================
.PHONY: setup generate-pot merge-po
setup: ## セットアップ - ビルドの前準備
setup: check generate-pot merge-po

generate-pot: $(addsuffix .pot,$(SRCS))

%.csv.pot: %.csv.toml $(D_SS)/%.csv
	@echo -e '$(CC_BrBlue)========== $@ ==========$(CC_Reset)'
	$(D_BIN)/csv2pot.py -c $<

%.json.pot: %.json.toml $(D_SS)/%.json
	@echo -e '$(CC_BrBlue)========== $@ ==========$(CC_Reset)'
	$(D_BIN)/json2pot.py -c $<

merge-po: $(addsuffix .edit.po,$(SRCS)) $(addsuffix .po,$(SRCS))

# ## edit.po の作成
# potとマージする静的なパターンルール
$(addsuffix .edit.po,$(SRCS)):: %.edit.po: %.pot
	@echo -e '$(CC_BrBlue)========== $@ 1 ==========$(CC_Reset)'
	if [[ -f "$@" ]] ; then \
		msgmerge --no-fuzzy-matching --backup=t -U $@ $< ; \
	else \
		msginit --no-translator -l ja_JP.utf8 -i $< -o $@ ; \
	fi

# ## edit.po の作成
# poとマージする静的なパターンルール
# 循環参照対策でPrerequisiteはつけない
# poファイルにpotをマージしてから、poと合わせる
$(addsuffix .edit.po,$(SRCS))::
	@echo -e '$(CC_BrBlue)========== $@ 2 ==========$(CC_Reset)'
	$(eval PO := $(@:%.edit.po=%.po))
	if [[ -f "$(PO)" ]] ; then \
		msgmerge --no-fuzzy-matching --backup=t -U $(PO) $(PO:%.po=%.pot) ; \
		msgcat --use-first -o $@ $@ $(PO) ; \
	fi

# ## po の作成
# edit.poとマージする静的なパターンルール
$(addsuffix .po,$(SRCS))::
	$(eval POT := $(@:%.po=%.pot))
	$(eval EP := $(@:%.po=%.edit.po))
	$(MAKE) $(EP)
	@echo -e '$(CC_BrBlue)========== $@ ==========$(CC_Reset)'
	if [[ -f "$@" ]] ; then \
		msgmerge --no-fuzzy-matching --no-location --no-wrap --backup=t -U $@ $(POT) ; \
		msgcat --use-first --no-location --no-wrap -o $@ $(EP) $@ ; \
	else \
		cp -f $(EP) $@ ; \
	fi ; \
	msgattrib --no-obsolete --no-location --no-wrap --sort-output -o - $@ \
	| grep -vE '^"(POT-Creation-Date|X-Generator):.*\\n"' \
	| sponge $@


#==============================================================================
# ビルド
#==============================================================================
.PHONY: build generate-mo translate copy-mod
build: ## ビルドする
build: setup generate-mo translate copy-mod

generate-mo: $(addsuffix .mo,$(SRCS))

%.mo: %.po
	@echo -e '$(CC_BrBlue)========== $@ ==========$(CC_Reset)'
	msgfmt --statistics -o $@ $^

translate: $(SRCS)

%.csv: %.csv.mo %.csv.toml $(D_SS)/%.csv
	@echo -e '$(CC_BrBlue)========== $@ ==========$(CC_Reset)'
	$(D_BIN)/mo2csv.py -m $< -c $@.toml

%.json: %.json.mo %.json.toml $(D_SS)/%.json
	@echo -e '$(CC_BrBlue)========== $@ ==========$(CC_Reset)'
	$(D_BIN)/mo2json.py -m $< -c $@.toml

copy-mod: $(SRCS)
	@echo -e '$(CC_BrBlue)========== $@ ==========$(CC_Reset)'
	@mkdir -p $(D_MOD)
	cp -u $^ $(D_MOD) || :


#==============================================================================
# クリーンアップ
#==============================================================================
.PHONY: clean clean-all clean-pot clean-mo clean-target clean-backup clean-package
clean: ## セットアップで生成したファイル以外を全て削除します
clean: clean-mo clean-target clean-package

clean-all: ## 生成した全てのファイルを削除します
clean-all: clean clean-pot clean-backup

clean-pot:
	@echo -e '$(CC_BrMagenta)========== $@ ==========$(CC_Reset)'
	rm -f *.pot

clean-mo:
	@echo -e '$(CC_BrMagenta)========== $@ ==========$(CC_Reset)'
	rm -f *.mo

clean-target:
	@echo -e '$(CC_BrMagenta)========== $@ ==========$(CC_Reset)'
	rm -f $(SRCS)

clean-backup:
	@echo -e '$(CC_BrMagenta)========== $@ ==========$(CC_Reset)'
	rm -f *~

clean-package:
	@echo -e '$(CC_BrMagenta)========== $@ ==========$(CC_Reset)'
	cd $(D_MOD) && rm -f $(SRCS)
