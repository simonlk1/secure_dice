# Prerequisites and System Specifications

Python 3 (I use 3.10.7)

rsa pip package (I use 4.9)

Bash (I use Git Bash)

Openssl (Included)

I am running on an x64 cpu, running Windows 10 Build 19044

# Running the Solution

From the root of the repository, run the following commands:

`$ ./generatekeys.sh`

`$ ./alice.py`

`$ ./bob.py`

# The Protocol

It is assumed that Bob and Alice have access to the following files: alice.public.pem, bob.public.pem, shared.py. Only Bob should be able to access bob.py and bob.private.pem. Only Alice should be able to access alice.py and alice.private.pem. After the environment is setup, neither Bob nor Alice will need to access generatekeys.sh nor openssl.exe.

Bob and Alice use RSA encryption as implemented by the rsa library to encrypt the messages they send each other, ensuring confidentiality. They use TLS as implemented by socket and ssl python libraries, ensuring integrity. Availability is not completely guaranteed. For example, they are both vulnerable to a DDoS attack.

For Bob and Alice to agree on the dice they roll, they use Pedersen Commitments. For this, they use the multiplicative group of integers module p, where p is a 16-bit prime and g is a primitive root module p. The bittage of p can be changed in shared.py, but due to inefficient algorithms this will slow down the program significantly.