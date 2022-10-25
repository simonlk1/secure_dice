#!/usr/bin/env bash

for name in "alice" "bob"; do
    # generate 4096-bit certificates for tls
    openssl req \
        -x509 \
        -newkey rsa:4096 \
        -keyout "$name.tls.key.pem" \
        -out "$name.tls.cert.pem" \
        -sha256 \
        -days 365 \
        -nodes \
        -subj "//CN=$name" \
        -addext "subjectAltName = DNS:localhost,DNS:$name"
done