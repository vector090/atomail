#!/bin/bash

# AtoMail script to convert POP3 emails to Atom feed
# Usage: ./run.sh

#MODE=
#HOST=
#USR=
#PASS=

DIR=gen
[ ! -e $DIR ] && mkdir -p $DIR

OUTF=$0.xml

python3 atomail.py \
  --mode $MODE \
  --host $HOST \
  --user $USR \
  --password $PASS \
  --uri http://example.com/feed.xml \
  --title $USR \
  --max-items=20 \
-d \
  $OUTF

mv $OUTF $DIR/

exit
#  -v \
--max-items=100 \
  --port 995 \

