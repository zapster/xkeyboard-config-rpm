# Makefile for source rpm: xkeyboard-config
# $Id$
NAME := xkeyboard-config
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
