import os
from private import *
import random
from random import randint

class Screen(object):
	'''
	Screen has-a Scoreboard
	Screen has-a Game
	     Game has-a Round
	          Round has-a GamePrompt
	'''
	def __init__(self):
		self.messages = GamePrompts()

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
	'''
	This class contains all on-screen messaging (including formatting)
	'''
	# this is passed
	#    guesses
	#    key.cheat
	#    key.scrambled_word
	#    key.ans
	lose_responses = ['Better luck next time!',
		'whooo boy, that was BRUTAL!',
		'Seriously dude?',
		'So annoying.',              
		'I bet one of those braindead motorcycle dudes from wolf street could have gotten that one!',
		'A valiant attempt.',
		'Welp, that sucked.',
		"This game kind of blows, doesn't it?",
		"Were those responses real??",
		"Oy vey!"
		] 
		
	input_prompts = ["[first guess]> ",
		"[try again]> ",
		"[one last try!]> "
		]	
	
	def __init__(self):
		self.stars = '*'*75
		self.dashes = '-'*75
		self.line = '_'*75
		
	def instructions(self, cheat):
		print ''
		print self.stars
		print 'GAME INSTRUCTIONS:'
		print ''
		print ' - Type in the correct spelling of the band.'
		print ' - You have three (3) chances to correctly guess.'
		print ' - Capitalization does NOT matter.'
		print ''
		print ' * You can type "%s" to re-scramble your clue.' % (cheat)
		print '   (However, it is only possilbe on your first guess'
		print '   as you will lose a guess when you re-scramble!!)'
		print ''
		print self.stars
		print '\n'		
	
	def clue(self, scrambled_word):
		print 'Here is your clue:'
		print '\n\t%s\n'% scrambled_word
	
	def new_clue(self, scrambled_word):
		print '\n'
		print 'Here is your NEW clue:'
		print '\n\t%s\n'% scrambled_word		
	
	def guess_prompt(self, guesses):
		return raw_input(self.input_prompts[guesses-1])
	
	def wrong_response(self):
		print "BZZZZEDDD!" 
		
	def win_response(self):
		print self.win_string.__doc__
	
	def lose_response(self, ans):		
		print self.lose_string.__doc__
		print 'The answer was:\n'
		print '     %s\n'% ans
		print self.lose_responses[randint(0, len(self.lose_responses)-1)]
		print ''
	
	def continue_message(self):
		print '\n'
		cont = raw_input('[Press "enter" to continue the game... or hit "Q" to quit]> ' )
		if cont.upper() != 'Q':
			print '\n'
		else:
			print '\nEnd game\n\nThanks for playing...\n\nRemember to "Like" us on facebook!\n\n'
			exit(1) 
			# it maybe shouldn't originate from here
			# but something in this area should call the EndGame() class
			# which has not been created yet
			
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
	
	

class KeyArgs(object):
	
	def __init__(self):
		self.scrambler = Scrambler()
		self.ans = self.scrambler.ans
		self.scrambled_word = self.scrambler.scram
		self.cheat = '?'
	
	def rescramble_word(self):
		return self.scrambler.word_scramble()