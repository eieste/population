import enum
import random
import config
import statistic


class LifeState(enum.IntEnum):
	CHILDHOOD = 1
	SEXUALLY_MATURE = 2
	PREGNANT = 3
	PARENT_TIME = 4
	SENIOR = 5
	ADULT = 6
	DEAD = 7
	
	
class Sex(enum.IntEnum):
	MALE = 1
	FEMALE = 2


def decision(probability):
	return random.random() < probability

def get_sex():
	if decision(config.SEX_RANDOM):
		return Sex.MALE
	return Sex.FEMALE



class Person:
	UPDATE_COUNT = 0
	POPULATION = []
	
	@staticmethod
	def get_count_of_living_person():
		c = 0
		for p in Person.POPULATION:
			if not p.has_state(LifeState.DEAD):
				c += 1
		return c

	def __init__(self, sex):
		self._sex = sex
		self._age = 0
		self._partner = None
		self._lifestate = LifeState.CHILDHOOD
		self._children = []
		
		# Collect stats
		if sex == Sex.MALE:
			statistic.AgeGroup.MALE_COUNT += 1
		else:
			statistic.AgeGroup.FEMALE_COUNT += 1


	def get_age(self):
		return self._age
		
	def has_state(self, state):
		return self._lifestate == state
			
	def get_orientation(self):
		if self._sex == Sex.MALE:
			return Sex.FEMALE
		return Sex.MALE
						
	def update_lifestate_change(self):
		#Childhood end
		if self._lifestate == LifeState.CHILDHOOD:
			
			if self._age > 16 and decision(config.CHILDHOOD_END_ABOVE_16) or \
				self._age > 18 and decision(config.CHILDHOOD_END_ABOVE_18) or \
				self._age > 20 and decision(config.CHILDHOOD_END_ABOVE_20):
				
				self._lifestate = LifeState.ADULT

				statistic.AgeGroup.ADULT_AGE += self._age
				statistic.AgeGroup.ADULT_AGE += 1
			
		# Adult end
		if self._lifestate in [LifeState.ADULT]:
			
			if self._age > 45 and decision(config.ADULT_TO_SENIOR_ABOVE_45) or \
				self._age > 50 and decision(config.ADULT_TO_SENIOR_ABOVE_50) or \
				self._age > 60 and decision(config.ADULT_TO_SENIOR_ABOVE_60):
				
				self._lifestate = LifeState.SENIOR		

				statistic.AgeGroup.SENIOR_AGE += self._age
				statistic.AgeGroup.SENIOR_COUNT += 1
				
	def in_love(self):
		
		if self._lifestate in [LifeState.ADULT]:
			
			if decision(config.ADULT_IN_LOVE) and self._partner is None:
				return True
		return False		
		
	def update_pragnet(self):
		
		if self.has_state(LifeState.PREGNANT):
			# Geburt weil person vorher schwanger war	
			children = 0
			if decision(config.PREGNANT_ABORT):
				# Fehlgeschlagene geburt
				pass
			elif decision(config.PREGNANT_TWINS):
				# Geburt von zwillingen
				children = 2
			else:
				# Einzelkind geburt
				children = 1

			statistic.AgeGroup.BIRTH_COUNT += 1
			for i in range(0, children):
				statistic.AgeGroup.CHILDREN_COUNT += 1
				p = Person(get_sex())
				self._children.append(p)
				Person.POPULATION.append(p)
	
			self._lifestate = LifeState.ADULT
		
		if self._lifestate == LifeState.ADULT and \
			self._partner is not None and \
			len(self._children) < config.MAX_CHILDREN_PER_FEMALE:
			
			if decision(config.ADULT_GET_PREGNANT) and \
				self._partner.has_state(LifeState.ADULT):
				
				statistic.AgeGroup.PREGNANT_AGE += self._age
				statistic.AgeGroup.PREGNANT_COUNT += 1
				self._lifestate = LifeState.PREGNANT
			
			
	def update(self):
		self._age += 1

		if not self.has_state(LifeState.DEAD):
			self.update_lifestate_change()
			
			if self._sex == Sex.FEMALE:
				self.update_pragnet()
		
	def dies(self):
		if self._lifestate != LifeState.SENIOR:
			dead = decision(config.PERSON_DIE)
			if dead:
				statistic.AgeGroup.DEAD_NOT_SENIOR_COUNT += 1
		else:
			dead = decision(config.SENIOR_DIE)
			if dead:
				statistic.AgeGroup.DEAD_SENIOR_COUNT += 1

		if dead and not self.has_state(LifeState.DEAD):
			self._lifestate = LifeState.DEAD
			statistic.AgeGroup.DEAD_COUNT += 1
			statistic.AgeGroup.DEAD_AGE += self._age
			if self._sex == Sex.MALE:
				statistic.AgeGroup.MALE_COUNT -= 1
			else:
				statistic.AgeGroup.FEMALE_COUNT -= 1


			#if self._partner.has_state(LifeState.DEAD):
			#	statistic.AgeGroup.COUPLE_COUNT -= 1


			return True
		return False
