#! /usr/bin/env python2
# -*- coding: utf-8  -*-
'''
Godel's Numbering
Copyright 2013 Gonzalo Ciruelos <comp.gonzalo@gmail.com> falziots @ github
Licensed under the Red Spider Project License.
See the License.txt that shipped with your copy of this software for details.
'''
import sys

# "Gödel's Proof", by Nagel and Newman.
SYMBOLS_NAGEL = {'~': 1,
				 '∨': 2,'v': 2,
				 '⊃': 3,
				 '∃': 4,
				 '=': 5,
				 '0': 6,
				 's': 7,
				 '(': 8,
				 ')': 9,
				 ':': 10,
				 '+': 11,
				 '*': 12}




def isprime(n):
	from math import sqrt

	if n==1 or n==0:
		return False
	elif n==2 or n==3:
		return True
	elif n%2==0:
		return False

	for div in range(3, int(sqrt(n)+1), 2):
		if n%div==0:
			return False

	return True


def factorize(n):
	div = 2

	factors = []

	while n!=1:
		while n%div==0:
			factors.append(div)
			n/=div
		div+=1

	return factors


def godelnumbertostring(godel):
	'''
	Factors the number and uses the table in the beginning of the script
	to translate it. The base is the order in the string and the exponent
	is the symbol.
	'''
	factors = sorted(factorize(int(godel)))

	inverted = {v: k for k, v in SYMBOLS_NAGEL.items()}

	string = []

	for n in range(2, max(factors)+1):
		if not isprime(n):
			continue

		string.append(inverted[factors.count(n)])

	return ''.join(string)


def stringtogodelnumber(string):
	'''
	Each token of the string is translated to a prime depending on the
	order of appearence (first token is two, second is three, etc), and
	it is exponentiated to the power that the table in the beginning of
	the script indicates.
	'''
	primes = generateprimes(2*len(string))

	godelnumber = 1

	for index in range(len(string)):
		try:
			prime = primes[index]
		except:
			print primes
			print index
		token = string[index]

		new = prime**(SYMBOLS_NAGEL[token])

		godelnumber *= new

	return godelnumber



def generateprimes(limit):
	'''
	Generates a list of primes for the stringtogodelnumber function.
	'''
	primes = [2]
	n = 3
	while limit>=0:
		if isprime(n):
			primes.append(n)
		n+=2
		limit-=1

	return primes


def main(argv = None):
	print

	if not argv:
		print helpMessage

	elif argv[0].lower() == 'number':
		try:
			print godelnumbertostring(int(argv[1]))
		except TypeError:
			print 'Error with the number, try again'
		except KeyError:
			print 'Error with the number: it doesn\'t correspond to a well-formed formula'
		except:
			print 'Error with the number, try again'

	elif argv[0].lower() == 'string':
		try:
			print stringtogodelnumber(argv[1])
		except:
			print 'Error with string, try again'

	else:
		print helpMessage

	print

helpMessage = '''
This is the help message for the godel command.

godel number <godel-number>  --> Translate a Gödel number to the correspondant string.
godel string <string>        --> Translate a string to the correspondant Gödel number.

The script uses the numbering from the book "Gödel's Proof", by Nagel and Newman.

Here are the math symbols that the program understands: ~, (∨; v), ⊃, ∃, =, 0, s, (, ), :, +, *.

Examples of use:

godel string ~ssss0=s0*ss0
godel number 243000000
'''

if __name__ == '__main__':
    main(sys.argv[1:])
