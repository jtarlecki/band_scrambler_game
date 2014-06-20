import os, sys
import random
from random import randint
from private import *

class Scorecard():
	
	def __init__(self):
		self.wins = 0
		self.games_played = 0
		self.guess_count = 0

	def update(self, guesses, won_game):
		self.games_played += 1
		self.guess_count += guesses
		self.wins += int(won_game)	
		self.correct_guess_percent = "%.2f" % ((float(self.wins)*100)/self.guess_count) + '%'
	
	def results(self):
		print ''
		print 'Your game stats'
		print '-----------------------------'
		print 'Games won: %d / %d' % (self.wins, self.games_played)
		print 'Correct guess percentage: %s' % (self.correct_guess_percent)
		print '-----------------------------'
		print ''

	def print_header(self, cheat):
		print 'ROUND: %d' % (self.games_played+1), 'GAMES WON: %d' % (self.wins)
		print 
		print ''
		print '*************************************************************************'
		print 'GAME INSTRUCTIONS:\n'
		print " - You have three (3) chances to correctly guess."
		print " - Capitalization does NOT matter.\n - Please guess OR type '%s' to re-scramble your clue." % (cheat)
		print "   (However, you will lose a guess if you re-scramble!!)"
		print ''
		print '*************************************************************************'
		print '\n\n'
		
def play_game(Scorecard):
	prompts = GamePrompts()
	
	s = Scrambler()
	ans = s.ans
	scram = s.scram
	
	clue = 'Here is your clue:'			# GamePromps class
	cheat = '*'							# comments class
	lose_response = ['Better luck next time!',
		'whooo boy, that was BRUTAL!',
		'Seriously dude?',
		'Weak attempt',
		'I bet one of those braindead motorcycle dudes from wolf street could have gotten that one!',
		'A valiant attempt.',
		'Welp, that sucked.',
		"This game kind of blows, doesn't it?",
		"Were those responses real??",
		"Oy vey!"
		] 
		
	input_prompt = ["[first guess]> ",
		"[try again]> ",
		"[one last try!]> "
		]	

	Scorecard.print_header(cheat)
	
	print clue
	print '\n     %s\n'% scram

	guesses = 1
	guess = raw_input(input_prompt[guesses-1])
	
	while guess.lower() != ans.lower() and guesses < 3:
		if guesses == 1 and guess.lower() == cheat:
			guesses +=2
			scram = s.word_scramble()
			print '\n' + clue.replace('clue', 'NEW clue')
			print '\n     %s\n'% scram
		else:
			print "BZZZZEDDD!"
			guesses += 1
		guess = raw_input(input_prompt[guesses-1])
	
	if guess.lower() == ans.lower():
		print prompts.win
		won = True
	else:
		print prompts.lose
		print 'The answer was:\n'
		print '     %s\n'% ans
		print lose_response[randint(0, len(lose_response)-1)]
		print ''
		won = False
	
	Scorecard.update(guesses, won)
	Scorecard.results()
	
	cont = raw_input('[Press "enter" to continue the game... or hit "Q" to quit]> ' )
	if cont.upper() != 'Q':
		print '\n'
	else:
		print '\nEnd game\n\nThanks for playing...\n\nRemember to "Like" us on facebook!\n\n'
		exit(1)
			


class Scrambler(object):
	
	def __init__(self):
		self.dirs = os.listdir(music_folder) 	# from private.py
		self.ans = self.get_band()
		self.split = self.split_words()
		self.scram = self.word_scramble()
		
	def get_band(self):
		band = self.dirs[randint(0, len(self.dirs)-1)]
		return band

	def split_words(self):
		words = self.ans.lower().split()
		return words

	def word_scramble(self):
		scrambled_phrase = []
		
		for word in self.split:
			scrambled_phrase.append(self.shuffle_letters(word))
		
		return ' '.join(scrambled_phrase).title()
			
	def shuffle_letters(self, word):
		letters = list(word)
		scramble = []
		
		while len(letters) > 0:
			letter = random.choice(letters)
			scramble.append(letter)
			letters.remove(letter)
		
		return ''.join(scramble)	
	

class GamePrompts(object):
	
	def __init__(self):
		self.win = self.win_string.__doc__
		self.lose = self.lose_string.__doc__
	
	def win_string():
		""" 
		W     W     W   WWWWWWW   WW     W
		 W   W W   W       W      W WW   W
		  W W   W W        W      W   WW W
		   W     W      WWWWWWW   W     WW 
		"""
		pass	
	def lose_string(): 
		"""
		            :(
					 
		:(        you lose        :(

		            :(
		"""
		pass	
	
	
class Engine(object):
	
	def __init__(self):
		self.start()
	
	def start(self):
		print '\n\n****NEW GAME***\n\n'
		s = Scorecard()

		while True:
			os.system('cls')
			play_game(s)
	
e = Engine()




