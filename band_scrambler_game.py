import os, sys
import random
import json
from random import randint
from private import *

'''
// TODO:

title screen

compare player1's score to the highscore,
if any are higher, prompt them for their name (under 8 digits)
and write it to the database (aka, json to .txt file)

break out some of the generic class manipulations from 
HighScore() class, they acaully have nothing to do with the 
class and are generic functions that could be used elsewhere

consolodate screen feedback into one area

make a Scoreboard.refresh() method to clean up updates to the board
clean up the code in this class

in Scoreboard class-- dynamic inputs of player1 and hi_score lists?
these could technically come from the classes themselves, in the right
order.. perhpas using some of the generic functions that need to 
broke out of the HighScore() class

organize this into a package.  It doens't need to be in one module.

dynamic reading of mp3 files?

store json of the entire music library locally??
allow user to refresh?
or allow user to define where the library is?
make a class to atleast allow for this in future
if i change the front end?
'''


class Scoreboard():
	
	def __init__(self, scorecard, highscore):
		self.player1 = scorecard
		self.highscore = highscore
		self.stars = '*'*75
		self.dashes = '-'*75
		self.line = '_'*75
		
	def refresh(self):
		# at the end of each round, this should control the updates
		pass

	def results(self):
		# // TODO: this might get the axe
		# with a running scoreboard, this is just redundant
		print ''
		print 'Your game stats'
		print self.dashes
		print 'Games won: %d / %d' % (self.player1.wins, self.player1.rounds_played)
		print 'Correct guess percentage: %s' % (self.player1.correct_guess_percent)
		print self.dashes
		print ''

	def print_header(self, cheat):
		
		def stringify_list(mylist):
			if type(mylist) == type([]):
				mylist = ''.join([pad_string(str(item)) for item in mylist])
			return mylist
			
		def pad_string(string):
			while len(string)<9:
				string = ' ' + string
			return pipe_cap(string)
		
		def pipe_cap(string):
			return string + ' |'
		
		parser = ClassParser()
		
		headers = ['','ROUNDS', 'WINS' , 'GUESSES', 'WIN %', 'GUESS %']
		
						
		player1 = ['PLAYER 1']
		hi_score = ['HI SCORE']
		
		player1.extend(parser.cls_prop_val_list_sorted(self.player1))
		hi_score.extend(parser.cls_prop_val_list_sorted(self.highscore.scores))
		
		'''
		
		player1= ['PLAYER 1',
		          self.player1.rounds_played,
		          self.player1.wins,
		          self.player1.guess_count,
		          self.player1.win_percent,
		          self.player1.correct_guess_percent
		          ]
		hi_score = ['HI SCORE',
		           self.highscore.scores.rounds_played,
		           self.highscore.scores.wins,
		           self.highscore.scores.guess_count,
		           self.highscore.scores.win_percent,
		           self.highscore.scores.correct_guess_percent
		           ]
		'''
		line = '='*len(stringify_list(headers))
		the_board = [headers, line, player1, hi_score, line]
		
		for item in the_board:
			print stringify_list(item)

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
	
		

class Scorecard():
	
	def __init__(self, 
	             rounds_played=0, 
	             wins=0, 
	             guess_count=0, 
	             win_percent='0.00%', 
	             correct_guess_percent='0.00%'):
		
		self.rounds_played = rounds_played
		self.wins = wins
		self.guess_count = guess_count
		self.win_percent = win_percent
		self.correct_guess_percent = correct_guess_percent

	def update(self, guesses, won_game):
		
		def calc_percent(num, denom):
			return "%.2f" % ((float(num)*100)/denom) + '%'
		
		self.rounds_played += 1
		self.wins += int(won_game)	
		self.guess_count += guesses
		self.win_percent = calc_percent(self.wins, self.rounds_played)
		self.correct_guess_percent = calc_percent(self.wins, self.guess_count)

		
def play_game(scoreboard):
	prompts = GamePrompts()
	
	s = Scrambler()
	ans = s.ans
	scram = s.scram
	
	clue = 'Here is your clue:'					# GamePromps class
	cheat = '?'							# comments class
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

	scoreboard.print_header(cheat)
	
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
	
	scoreboard.player1.update(guesses, won)
	scoreboard.results()
	
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
	'''
	so many initializations of Scorecard()
	think about passing that in as a parameter to this class.
	I count five (5) instances
	But there may not be any benefit
	I may be going overboard with making everything generic.
	'''
	def __init__(self):
		
		# read_scores() and write_scores() methods close the log file

		self.filename = 'high_scores.txt'
		self.score_list = None
		self.parser = ClassParser()
		
		try:
			self.read_scores()
		except:
			self.open_scores('w')
		
		self.init_classes()

	
	def open_scores(self, mode='r'):
		self.score_log = open('%s' % (self.filename), mode)		
		
	def read_scores(self):
		self.open_scores('r')
		self.json_scores_text = self.score_log.read()
		self.json_scores_python = json.loads(self.json_scores_text)
		self.score_log.close()
		
		print 'self.json_scores_text: '
		print self.json_scores_text
		print 'json_scores_python: ', self.json_scores_python
		
	def write_scores(self, scores_json_format):
		self.open_scores('w')
		self.score_log.write(scores_json_format)
		self.score_log.close()
	
	def close(self):
		self.score_log.close()
	
	def create_json(self):
		self.json_scores_python = {'scores': self.parser.class_to_dict(self.scores),
		                           'owners': self.parser.class_to_dict(self.owners)}
		self.json_scores_text = json.dumps(self.json_scores_python,
		                                   sort_keys=True,
		                                   indent=4,
		                                   separators=(',', ': '))			
		
		print 'self.json_scores_python:', self.json_scores_python
		print 'self.json_scores_text:'
		print self.json_scores_text
	
	def init_classes(self):
		if self.json_scores_python == None:
			self.scores = Scorecard()
			self.owners = Scorecard(*len(Scorecard().__dict__)*['---'])
			self.create_json() 
			self.write_scores(self.json_scores_text)
		else:
			self.scores = self.parser.dict_to_cls(self.json_scores_python['scores'], Scorecard())
			self.owners = self.parser.dict_to_cls(self.json_scores_python['owners'], Scorecard())
			# json already exists
			# scores came from database

class ClassParser(object):
	
	def __init__(self):
		pass
	
	# called from outside class
	def class_to_dict(self, cls):
		# turns a class into a dictionary
		d = {}
		for key in cls.__dict__:
			d[key] = cls.__dict__[key]
		return d
		
	# called from outside class
	def dict_to_cls(self, dictionary, cls):
		'''
		pass in a dictionary and a dummy class instance
		and get a new instance of that class,
		instantiated with the arguments from that dictionary
		'''
		args = []
		for cls_prop in self.cls_prop_name_list_sorted(cls):
			args.append(dictionary[cls_prop])
		return cls.__class__(*args)

	def cls_prop_name_list_sorted(self, cls):			
		# clsName:
		# True = Return the class property names
		# False = Return the instance's property vaules
		'''
		first, get a ranked list of class arguments as a list of tuples
		then, sort the tuples by the rank number (asc)
		finally, pull the sorted class property names out
		and return them in an ordered list
		'''
		cls_numbered = cls.__class__(*[i for i in range(len(cls.__dict__))])
		cls_tuples = sorted(cls_numbered.__dict__.items(), key=lambda prop: prop[1])
		cls_list = []
		
		for item in cls_tuples:
			cls_list.append(item[0])
		return cls_list
	
	def cls_prop_val_list_sorted(self, cls):
		prop_name_list = self.cls_prop_name_list_sorted(cls)
		d = self.class_to_dict(cls)
		sorted_list = []
		for prop in prop_name_list:
			sorted_list.append(d[prop])
		return sorted_list
		
class Engine(object):
	
	def __init__(self):
		self.start()
	
	def start(self):
		print '\n\n****NEW GAME***\n\n'
		
		scoreboard = Scoreboard(Scorecard(),HighScores())

		while True:
			os.system('cls')
			play_game(scoreboard)
	

def run():
	e = Engine()

def test():
	# wins=0, rounds_played=0, guess_count=0, correct_guess_percent='0.00%'
	h = HighScores()

if __name__ == '__main__':
	run()


