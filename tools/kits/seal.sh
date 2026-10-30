#!/bin/bash
# seal.sh <file.pdf> <out_dir> : encrypts a paid file so only GitHub Actions (KIT_PRIVATE_KEY) can open it
set -e; f="$1"; o="$2"; mkdir -p "$o"; k=$(openssl rand -hex 32)
openssl enc -aes-256-cbc -pbkdf2 -salt -in "$f" -out "$o/file.enc" -pass pass:$k
printf "%s" "$k" | openssl pkeyutl -encrypt -pubin -inkey "$(dirname "$0")/kit_public.pem" -out "$o/key.enc"
echo sealed "$o"
