import sys
import entity


class AgeGroup:
	
	FEMALE_COUNT = 0
	MALE_COUNT = 0

	CHILDREN_COUNT = 0
	BIRTH_COUNT = 0

	ADULT_AGE = 0
	ADULT_COUNT = 0

	COUPLE_COUNT = 0
	
	DEAD_AGE = 0
	DEAD_COUNT = 0
	DEAD_NOT_SENIOR_COUNT = 0
	DEAD_SENIOR_COUNT = 0

	PREGNANT_AGE = 0
	PREGNANT_COUNT = 0

	SENIOR_AGE = 0
	SENIOR_COUNT = 0


	def __init__(self, minage, maxage):
		self._minage = minage
		self._maxage = maxage
		
		self._p = []
		
		self._pregnant = 0
		self._dead = 0
		self._couple = 0
		self._children = 0

	def age_in(self, age):
		if age > self._minage and age < self._maxage:
			return True
		return False
		
	def add(self, person):		
		
		if person.has_state(entity.LifeState.DEAD):
			self._dead += 1
			
		if person._partner is not None:
			self._couple += 0.5
			
		if person.has_state(entity.LifeState.PREGNANT):
			self._pregnant += 1
		
		for c in person._children:
			if c.has_state(entity.LifeState.CHILDHOOD):
				self._children += 1

		if person._partner is not None:
			AgeGroup.COUPLE_COUNT += 1



		self._p.append(person)


def collect_info(person):
	
	age_group = [
		AgeGroup(0, 10),	
		AgeGroup(10, 20),
		AgeGroup(20, 30),
		AgeGroup(30, 40),
		AgeGroup(40, 50),
		AgeGroup(50, 60),
		AgeGroup(60, 70),
		AgeGroup(80, 90),
		AgeGroup(90, 100),
		AgeGroup(100, 200),
	]
	
	
	for p in person.POPULATION:
		
		for a in age_group:
			
			if a.age_in(p.get_age()):
				a.add(p)
	return age_group
	
def seperator():
	return "|".ljust(3).rjust(3)
	
def inplace(text, place):
	return str(text).rjust(3).ljust(place)
	
def printval(name, value):
	txt = ""
	txt += inplace(name, 40)
	txt += seperator()
	txt += inplace(value, 20)
	txt += "\n"
	return txt


def display_info(person):
	collected_info = collect_info(person)
	
	txt = ""
	
	txt += inplace("Altersgruppe", 15)
	txt += seperator()
	txt += inplace("Count", 10)
	txt += seperator()
	txt += inplace("Schwanger", 15)
	txt += seperator()
	txt += inplace("Tot", 5)
	txt += seperator()
	txt += inplace("Paare", 10)
	txt += seperator()
	txt += inplace("Kinder", 10)
	
	txt += "\n"
	txt += "-"*len(txt)
	txt += "\n"

	for item in collected_info:
		txt += inplace("{} - {}".format(item._minage, item._maxage), 15)
		txt += seperator()
		txt += inplace(len(item._p), 10)
		txt += seperator()
		txt += inplace(item._pregnant, 15)
		txt += seperator()
		txt += inplace(item._dead, 5)
		txt += seperator()
		txt += inplace(int(item._couple), 10)
		txt += seperator()
		txt += inplace(int(item._children), 10)
		txt += "\n"

	txt += "\n"
	txt += "\n"
	txt += "\n"

	txt += inplace("Name", 40)
	txt += seperator()
	txt += inplace("Value", 20)
	txt += "\n"
		
	popcount = person.get_count_of_living_person()
		
	txt += printval("Iteration", person.UPDATE_COUNT)
	txt += printval("Population", person.get_count_of_living_person())
	txt += printval("Zeugungsfähige Paare", len([item for item in person.POPULATION if item.has_state(entity.LifeState.ADULT)]))


	txt += printval("% Frauen", AgeGroup.FEMALE_COUNT/(popcount)*100)
	txt += printval("% Männer", AgeGroup.MALE_COUNT/(popcount)*100)

	if AgeGroup.PREGNANT_AGE != 0 and AgeGroup.PREGNANT_COUNT != 0:
		txt += printval("Ø Schwangerschaftsalter", AgeGroup.PREGNANT_AGE/AgeGroup.PREGNANT_COUNT)

	if AgeGroup.BIRTH_COUNT != 0 and AgeGroup.PREGNANT_COUNT:
		txt += printval("Ø Geburten pro Schwangerschaft", AgeGroup.BIRTH_COUNT/AgeGroup.CHILDREN_COUNT)

	if AgeGroup.DEAD_COUNT != 0 and AgeGroup.DEAD_COUNT:
		txt += printval("Ø Sterbealter", AgeGroup.DEAD_AGE/AgeGroup.DEAD_COUNT)
	
	if AgeGroup.DEAD_NOT_SENIOR_COUNT != 0 and AgeGroup.DEAD_COUNT:
		txt += printval("Ø Zu früh gestorben", AgeGroup.DEAD_NOT_SENIOR_COUNT/AgeGroup.DEAD_COUNT)
	
	
	if AgeGroup.COUPLE_COUNT != 0 and AgeGroup.CHILDREN_COUNT:
		txt += printval("Ø Kinder pro Paar", AgeGroup.CHILDREN_COUNT/AgeGroup.COUPLE_COUNT)
	
	print(txt)
	return len(txt)
