# SPDX-License-Identifier: MIT
# Copyright 2023 hirmiura (https://github.com/hirmiura)
#
SHELL := /bin/bash

# 各種ディレクトリ
D_REL		:= ../..
D_BIN		:= $(D_REL)/bin
D_SUBPATH	:= data/campaign
D_MOD		:= $(D_REL)/mod/$(D_SUBPATH)
D_SS		:= $(D_REL)/Starsector/starsector-core/$(D_SUBPATH)

# ソース
SRCS := $(basename $(shell ls *.{csv,json}.toml))


#==============================================================================
# 翻訳ディレクトリ共通Makefile
#==============================================================================
include ../TransCommon.mk
