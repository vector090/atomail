#!/bin/bash

# AtoMail script to convert POP3 emails to Atom feed
# Usage: ./run.sh

python3 atomail.py \
  --mode imap \
  --host v90.pp.ua \
  --port 50143 \
  --user u1@local.nuc \
  --password 123456 \
  --uri http://example.com/feed.xml \
  --title "My POP3 Feed" \
  -d \
  $0.xml

exit
