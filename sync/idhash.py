#!/usr/bin/env python3
"""The repo is public, so Drive file ids are never stored in it — only a short hash of each id.
  python3 sync/idhash.py ID [ID ...]     prints  ID  HASH  for each
"""
import hashlib, sys


def idhash(file_id):
    return hashlib.sha256(file_id.strip().encode()).hexdigest()[:16]


if __name__ == "__main__":
    for i in sys.argv[1:]:
        print(i, idhash(i))
