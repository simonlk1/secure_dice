import math
import random

MAX_ROLL = 6
PRIME_BITS = 16
ALICE_PORT = 24440
BOB_PORT = 24441
PORT = 24442
HOST = "localhost"

def generate_dice_roll():
    return random.randint(1, MAX_ROLL)

def agree_on_roll(r1, r2):
    return ((r1 + r2) % 6)+1

def compute_commit(m, r):
    return 1

def is_prime(n):
  for i in range(2,int(math.sqrt(n))+1):
    if (n%i) == 0:
      return False
  return True

# Large Prime Generation, taken from https://www.geeksforgeeks.org/how-to-generate-large-prime-numbers-for-rsa-algorithm/

# Pre generated primes
first_primes_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
					31, 37, 41, 43, 47, 53, 59, 61, 67,
					71, 73, 79, 83, 89, 97, 101, 103,
					107, 109, 113, 127, 131, 137, 139,
					149, 151, 157, 163, 167, 173, 179,
					181, 191, 193, 197, 199, 211, 223,
					227, 229, 233, 239, 241, 251, 257,
					263, 269, 271, 277, 281, 283, 293,
					307, 311, 313, 317, 331, 337, 347, 349]

def nBitRandom(n):
	return random.randrange(2**(n-1)+1, 2**n - 1)

def getLowLevelPrime(n):
	'''Generate a prime candidate divisible
	by first primes'''
	while True:
		# Obtain a random number
		pc = nBitRandom(n)

		# Test divisibility by pre-generated
		# primes
		for divisor in first_primes_list:
			if pc % divisor == 0 and divisor**2 <= pc:
				break
		else: return pc

def isMillerRabinPassed(mrc):
	'''Run 20 iterations of Rabin Miller Primality test'''
	maxDivisionsByTwo = 0
	ec = mrc-1
	while ec % 2 == 0:
		ec >>= 1
		maxDivisionsByTwo += 1
	assert(2**maxDivisionsByTwo * ec == mrc-1)

	def trialComposite(round_tester):
		if pow(round_tester, ec, mrc) == 1:
			return False
		for i in range(maxDivisionsByTwo):
			if pow(round_tester, 2**i * ec, mrc) == mrc-1:
				return False
		return True

	# Set number of trials here
	numberOfRabinTrials = 20
	for i in range(numberOfRabinTrials):
		round_tester = random.randrange(2, mrc)
		if trialComposite(round_tester):
			return False
	return True

def generate_prime(bits):
    while True:
        prime_candidate = getLowLevelPrime(bits)
        if not isMillerRabinPassed(prime_candidate):
            continue
        else:
            return prime_candidate

# Parts taken from https://github.com/lorenzogentile404/pedersen-commitment/blob/master/pedersen-commitment.py
def generate_group():
        p = generate_prime(PRIME_BITS)

        r = 1
        while True:
            q = r*p + 1
            if is_prime(q):
                break
            r += 1
        
        G = [] 
        for i in range(1, q):
            G.append(i**r % q)

        G = list(set(G))

        g = random.choice(list(filter(lambda e: e != 1, G)))

        h = random.choice(list(filter(lambda e: e != 1 and e != g, G)))
           
        return q,g,h

Q, H, G = generate_group()