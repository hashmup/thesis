#!/usr/bin/env perl
# $latex = "find . -type f -name '*.tex' | xargs sed -i '' -e 's/、/，/g' -e 's/。/．/g'; uplatex -synctex=1 -halt-on-error %O %S";
$biber = 'biber --bblencoding=utf8 -u -U --output_safechars';
