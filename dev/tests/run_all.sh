#!/bin/sh
# Extract the app script from index.html, syntax-check everything, then run the mock harness for every region.
cd "$(dirname "$0")"
python extract_app.py || exit 1
node --check m3.js || exit 1
for f in ../../regions/*.js; do node --check "$f" || exit 1; done
for id in vic nsw qld wa sa tas act nt; do
  REGION_FILE=../../regions/$id.js node harness_region.js > out_$id.txt 2>&1
  if grep -q "ERR\|Error" out_$id.txt; then echo "$id FAILED"; tail -5 out_$id.txt; else echo "$id ok: $(head -1 out_$id.txt)"; fi
done
