import os, sys
import random
import json
from random import randint
from private import *

class Scorecard():
	
	def __init__(self, wins=0, rounds_played=0, guess_count=0, correct_guess_percent='0.00%'):
		self.wins = wins
		self.rounds_played = rounds_played
		self.guess_count = guess_count
		self.correct_guess_percent = correct_guess_percent

	def update(self, guesses, won_game):
		self.rounds_played += 1
		self.guess_count += guesses
		self.wins += int(won_game)	
		self.correct_guess_percent = "%.2f" % ((float(self.wins)*100)/self.guess_count) + '%'
	
	def results(self):
		print ''
		print 'Your game stats'
		print '-----------------------------'
		print 'Games won: %d / %d' % (self.wins, self.rounds_played)
		print 'Correct guess percentage: %s' % (self.correct_guess_percent)
		print '-----------------------------'
		print ''

	def print_header(self, cheat):
		print 'ROUND: %d' % (self.rounds_played+1), 'GAMES WON: %d' % (self.wins)
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
	
	clue = 'Here is your clue:'					# GamePromps class
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

class HighScores(object):
# wins=0, rounds_played=0, guess_count=0, correct_guess_percent='0.00%'
	def __init__(self):
		self.filename = 'high_scores.txt'
		self.score_list = None
		try:
			self.open_scores('r')
			self.score_log.close()
		except:
			self.open_scores('w')
			self.scores = Scorecard()
			self.owners = Scorecard(*4*['---'])
			
			# this is work in progress... 
			# works great, just needs to be organized
			self.create_json() # test call
			
			self.write_scores(self.json_scores_text)
				
			self.score_log.close()
			
	def open_scores(self, mode='r'):
		self.score_log = open('%s' % (self.filename), mode)		
		
	def read_scores(self):
		self.open_scores('r')
		self.raw_score_list = self.score_log.read()
		print 'raw_score_list', list(self.raw_score_list)
		self.score_log.close()
		
	def write_scores(self, score_list):
		self.open_scores('w')
		self.score_list = score_list
		self.score_log.write(score_list)
		self.score_log.close()
	
	def close(self):
		self.score_log.close()
	
	def create_json(self):

		created_json = {'scores': self.class_to_dict(self.scores),
		                'owners': self.class_to_dict(self.owners)}
		
		print 'created_json', created_json
		
		print 'pretty print:'
		print json.dumps(created_json, sort_keys=True, indent=4, separators=(',', ': '))
		
		self.json_scores_python = created_json
		self.json_scores_text = json.dumps(created_json, sort_keys=True, indent=4, separators=(',', ': '))

	def class_to_dict(self, cls):
		# turns a class into a dictionary
		d = {}
		for key in cls.__dict__:
			d[key] = cls.__dict__[key]
		return d
		
	### not used ###
	def unpack_scores(self):
		self.highscores_list = []
		self.owners_list = []
		for s in self.raw_score_list:
			self.highscores_list.append(s[0])
			self.owners_list.append(s[1])
		highscores = Scorecard(*self.highscores_list)
		owners = Scorecard(*self.owners_list)
		print 'unpacked'
		
class Engine(object):
	
	def __init__(self):
		self.start()
	
	def start(self):
		print '\n\n****NEW GAME***\n\n'
		
		s = Scorecard()

		while True:
			os.system('cls')
			play_game(s)
	

def run():
	e = Engine()

def test():
	# wins=0, rounds_played=0, guess_count=0, correct_guess_percent='0.00%'
	scores = {'scores': 
	          {'wins': 0,
	           'rounds_played': 0,
	           'guess_count': 0, 
	           'correct_guess_percent': '45.45%'
	           },
	          'owners':
	          {'wins': "JT",
	           'rounds_played': "DAD",
	           'guess_count': "MOM", 
	           'correct_guess_percent': "PEN"
	           }
	          }
	scores_json = json.dumps(scores, sort_keys=True, indent=4, separators=(',', ': '))
	print scores_json
	python_obj = json.loads(scores_json)
	print python_obj['owners']
	print python_obj['scores']
	
	h = HighScores()
	#h.read_scores()
	#h.unpack_scores()

test()


