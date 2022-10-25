#!/usr/bin/env bash

for name in "alice" "bob"; do
    openssl genrsa -out $name.private.pem 4096
    pyrsa-priv2pub -i $name.private.pem -o $name.public.pem
done