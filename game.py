import os, sys
import json
from random import randint

import time
from messages import GamePrompts, KeyArgs

'''
// TODO:

title screen

compare player1's score to the highscore,
if any are higher, prompt them for their name (under 8 digits)
and write it to the database (aka, json to .txt file)

consolodate screen feedback into one area

make a Scoreboard.refresh() method to clean up updates to the board
clean up the code in this class

25 game champion
series 25*(n*2) (for n = 1 to inf)

organize this into a package.  It doens't need to be in one module.

dynamic reading of mp3 files?

store json of the entire music library locally??
allow user to refresh?
or allow user to define where the library is?
make a class to atleast allow for this in future
if i change the front end?
'''


class Scoreboard():
	'''
	Scoreboard has-a Scorecard
	Scoreboard has-a Highscore
	'''
	def __init__(self, scorecard, highscore):
		self.player1 = scorecard
		self.highscore = highscore
		self.stars = '*'*75
		self.dashes = '-'*75
		self.line = '_'*75
		self.milestones = [25,50,100,250,500,1000,2500,5000] 
		# i figured out the mathematical way to represent this odd series
		# put this in-- maybe include in KeyArgs class instead
		
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

	def print_header(self):
		
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
		
		parser = ClassParser() # lives and dies in this function call
		
		# // TODO: make headers a class upon initializing??? they don't change!
		'''
		self.rounds_played = rounds_played
		self.wins = wins
		self.guess_count = guess_count
		self.win_percent = win_percent
		self.correct_guess_percent = correct_guess_percent
		self.hole_in_1s = hole_in_1s		
		self.win_streak = win_streak

		'''
		headers = ['','ROUNDS', 'WINS' , 'GUESSES', 'WIN %', 'GUESS %', 'HOLE IN 1', 'WIN STR']
		player1 = ['PLAYER 1']
		hi_score = ['HI SCORE']
		player1.extend(parser.cls_prop_val_list_sorted(self.player1))
		hi_score.extend(parser.cls_prop_val_list_sorted(self.highscore.scores))
		
		line = '='*len(stringify_list(headers))
		the_board = [headers, line, player1, hi_score, line]
		
		for item in the_board:
			print stringify_list(item)


	def milestone_check(self):

		def milestone_message():

			message = 'Milestone Achieved!!!'
			acc_string = []
			for letter in message:
				os.system('cls')
				print '\n'*10
				acc_string.append(letter)
				print '\t'*2 + ' '.join(acc_string)
				time.sleep(0.2)
				print '\n'*10
			print '\t\t\t%s rounds played!' % (str(self.player1.rounds_played))
			
		def record_breaker_message():
			print ''
			print '\tand...'
			print ''
			print '\t\tYou just broke the record for %s' % ('rounds played')
			print '\t\twith %s %s ! ! !' % (self.player1.rounds_played, 'rounds played')
			print '\n'*10
		
		if self.player1.rounds_played in self.milestones:
			milestone_message()
		if 1==1: # test to see if records was broken
			pass
			#record_breaker_message()
			# // TODO
			# ask user for their initials
			# write record to database
			
			

class Scorecard():
	'''
	A scorecard with items to be recorded or retrieved
	'''
	def __init__(self, 
	             rounds_played=0, 
	             wins=0, 
	             guess_count=0, 
	             win_percent='0.00%', 
	             correct_guess_percent='0.00%',
	             hole_in_1s=0,	             
	             win_streak=0):
		
		self.rounds_played = rounds_played
		self.wins = wins
		self.guess_count = guess_count
		self.win_percent = win_percent
		self.correct_guess_percent = correct_guess_percent
		self.hole_in_1s = hole_in_1s		
		self.win_streak = win_streak

	def update(self, guesses, won_game):
		
		def calc_percent(num, denom):
			return "%.2f" % ((float(num)*100)/denom) + '%'
		
		if won_game:
			self.wins += 1
			self.win_streak += 1
		else:
			self.win_streak = 0
		
		self.rounds_played += 1
		if guesses==1:
			self.hole_in_1s += 1
		self.guess_count += guesses
		self.win_percent = calc_percent(self.wins, self.rounds_played)
		self.correct_guess_percent = calc_percent(self.wins, self.guess_count)
		
		
		
class Round(object):
	# this class needs some serious work
	# does a Screen have-a Round?
	
	def __init__(self, scoreboard):
		self.scoreboard = scoreboard
		self.play()
		
	def play(self):
		key = KeyArgs()
		display = GamePrompts()
		scoreboard = self.scoreboard
		
		# local assigments
		ans = key.ans.lower()		# local guess is lowercase
		scram = key.scrambled_word
		guess_limit = 3
		guesses = 1
		
		#-------------HEADER-------------#	
		scoreboard.print_header()
		display.instructions(key.cheat)
		
		#-------------BODY---------------#
		display.clue(scram)
		guess = display.guess_prompt(guesses).lower()
		
		while guess != ans and guesses < guess_limit:
			if guesses == 1 and guess.lower() == key.cheat:
				guesses +=2
				scram = key.rescramble_word()
				display.new_clue(scram)
			else:
				display.wrong_response()
				guesses += 1
			guess = display.guess_prompt(guesses).lower()
		
		if guess == ans:
			display.win_response()
			won = True
		else:
			display.lose_response(key.ans)
			won = False
		
		scoreboard.player1.update(guesses, won)
		scoreboard.milestone_check()		# this is a game operation
		
		#-------------FOOTER-------------#
		scoreboard.results() 			# this could be phased out		
		display.continue_message()

			
class HighScores(object):
	'''
	HighScore is-a scorecard
	'''
	#so many initializations of Scorecard()
	#think about passing that in as a parameter to this class.
	#I count five (5) instances
	#But there may not be any benefit
	#I may be going overboard with making everything generic.
	def __init__(self):
		# read_scores() and write_scores() methods close the log file
		self.filename = 'high_scores.txt'
		self.score_list = None
		self.parser = ClassParser()
		self.json_scores_python = None
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
		self.json_scores_python = {'scores': self.scores.__dict__,
		                           'owners': self.owners.__dict__
		                           }
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
		sorted_list = []
		for prop in prop_name_list:
			sorted_list.append(cls.__dict__[prop])
		return sorted_list
		
class Play(object):
	
	def __init__(self):
		self.start()
	
	def start(self):
		print '\n\n****NEW GAME***\n\n'
		
		scoreboard = Scoreboard(Scorecard(),HighScores())

		while True:
			os.system('cls')
			rnd = Round(scoreboard)
	

def run():
	p = Play()

def test():
	# wins=0, rounds_played=0, guess_count=0, correct_guess_percent='0.00%'
	h = HighScores()

if __name__ == '__main__':
	run()


