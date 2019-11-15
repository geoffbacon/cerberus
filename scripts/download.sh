#!/bin/bash
## Usage: download.sh
##
## Downloads and unpacks the Universal Dependencies corpora.
##
## At the time of writing, the latest version of the Universal Dependencies
## data is version 2.5, and this version is hard coded in.
DIR=back/ud/data/raw
wget --quiet -O ud.tgz https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11234/1-3105/ud-treebanks-v2.5.tgz
tar zxf ud.tgz -C $DIR
mv $DIR/ud-treebanks-v2.5/* $DIR
rmdir $DIR/ud-treebanks-v2.5
rm ud.tgz