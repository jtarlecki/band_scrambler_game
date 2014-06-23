import os

class Console(object):
	'''	
	Console has-a Game
	Console has-a HighScore
	Console has-a titlescreen
	    Game has-a Player
	    Game has-a Scoreboard
	        Scoreboard has-a HighScore_Scorecard
		Scoreboard has-a Game_Scorecard
	    Game has-a titlescreen
	    Game has-a instruction-rules
	    Game has milestones
	         milestone has-a HighScore
		 milestone has-a splashscreen
	    X--Game has-a Scorecard
	    Game has Rounds
	        Round has Rules
	        Round has GamePrompts
	        Round has-a Engine
	            Engine has-a answer
		    Engine has-a Scrambler
		        Scrambler has-a scrambled_word
	
	Highscore has-a Scorecard
	Game has-a Scorecard
	
	## these methods just assist
	Scoreboard has-a ClassParser 
	HighScore has-a ClassParser
	'''
	def __init__(self):
		self.game = Game()
		self.highscore = HighScore()
		self.title_screen()
		
	def title_screen(self):
		# print something
		pass

class Game(object):
	
	def __init__(self):
		self.player = Player()
		self.rules = Rules()
		self.scoreboard = Scoreboard()
		self.milestones = Milestones()
		self.start()
		
	
	def start(self):
		# welcome screen
		# instructions
		# ask for players name?
		# begin game
		while True:
			r = Round()
		pass
		
	def welcome_screen(self):
		pass
	
	def end(self):
		pass

class Rules(object):
	'''
	insert instruction block
	this could be called with __doc__ method
	'''
	def __init__(self):
		self.guess_limit = 3
		self.cheat = '?'
	
	def submit_guess(self, guess):
		if guess == self.cheat:
			# rescramble word
			# add 2 to guess
			return 2
		else:
			return 1
	
	def ok_to_guess(guess, ans, guesses):
		return guess != ans and guesses < self.guess_limit

class Player(object):
	
	def __init__(self, name):
		self.name = name
		self.scorecard = Scorecard()

class Round(object):
	
	def __init__(self):
		os.system('cls')

class Milestones(object):
	
	def __init__(self):
		self.rounds = self.get_rounds()
		self.highscores = self.get_milestone_highscores()
	
	def generate_milestone_rounds(self):
		# insert sequence code
		pass
	
	def get_milestone_highscores(self):
		for r in self.rounds:	
			# create dictionary of milestones
			pass
	
	def spash_screen(self):
		pass
	
class Scoreboard(object):
	
	def __init__(self):
		self.scorekeeper = ScoreKeeper()
		self.highscore = Scorecard('''retrieve high scores''')
		self.player1 = Scorecard()
