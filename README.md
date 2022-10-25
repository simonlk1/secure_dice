# Prerequisites and System Specifications

Python 3 (I use 3.11.0)

Bash (I use Git Bash)

OpenSSL (Included)

I am running on an x64 cpu, running Windows 10 Build 19044

# Running the Solution

From the root of the repository, run the following commands:

`$ ./generatekeys.sh`

`$ ./alice.py`

`$ ./bob.py`

# The Protocol

It is assumed that Bob and Alice have access to the following files: shared.py, alice.tls.cert.pem, bob.tls.cert.pem. It is assumed that only Alice has access to alice.py and alice.tls.key.pem. It is assumed that only Bob has access to bob.py and bob.tls.key.pem. After the environment is set-up, neither openssl.exe nor generatekeys.sh is needed.

Bob and Alice use TLS to communicate as implemented by the python ssl and socket libraries. TLS is used to guarantee confidentiality and integrity. Availability is limited in the sense that neither Alice nor Bob have ways of preventing all attacks, for example Denial of Service. To ensure that both parties have agency in the dice roll, Pedersen Commitments are used with the group of integers in the range [1..q] to the power of p mod q, where p and q are primes. In this example p and q have been generated as 16-bit primes due to inefficient algorithms otherwise slowing the program down significantly. This can be improved by re-generating with a call to generate_prime(n). Both roll a die in the range [1..6], the final die roll is given by computing ((roll1 + roll2) % 6) + 1

The protocol order and high-level execution of the implementation is as follows: Alice opens a port for Bob -> Bob connects with a valid certificate, otherwise disconnect -> Alice rolls and commits, sending commit to Bob -> Bob rolls and commits, sending commit to Alice -> Alice sends roll and r to Bob -> Bob sends roll and r to Alice -> They both verify the commit and agree on a dice roll.
