#!/bin/bash
## Usage: download.sh
##
## Downloads and unpacks the Universal Dependencies corpora.
##
## At the time of writing, the latest version of the Universal Dependencies
## data is version 2.4, and this version is hard coded in.
DIR=back/ud
wget --quiet -O ud.tgz https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11234/1-2988/ud-treebanks-v2.4.tgz
tar zxf ud.tgz -C $DIR
mv $DIR/ud-treebanks-v2.4 $DIR
rm ud.tgz