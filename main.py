from entity import Person, Sex, LifeState
import time
import statistic
import matplotlib.pyplot as plt
import matplotlib.animation as animation

Person.POPULATION = [Person(Sex.MALE), Person(Sex.FEMALE)]

OUT_LN = 0

CIRCLE = 0

LOVE_MATCH = []

PLOT = {
	"POPULATION": [],
	"BIRTH": []
}

#plt.ion()
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)



def main(i):

	CIRCLE = i
	LOVE_MATCH = []
	Person.UPDATE_COUNT += 1
	for p in Person.POPULATION:
		
		p.update()
		
		if p.dies():
			if p.get_age() > 150:
				del Person.POPULATION[Person.POPULATION.index(p)]
				# Person.POPULATION.pop(Person.POPULATION.index(p))

		if p.in_love():
			LOVE_MATCH.append(p)
	

	for i, lover in enumerate(LOVE_MATCH):

		if lover.has_state(LifeState.ADULT) and lover._partner is None:
						
			for partner in LOVE_MATCH + Person.POPULATION:
				if partner.has_state(LifeState.ADULT) and \
					partner._partner is None and \
					partner._sex == lover.get_orientation() and  \
					lover._sex == partner.get_orientation():

					lover._partner = partner
					partner._partner = lover

	OUT_LN = statistic.display_info(Person)
	
	PLOT["POPULATION"].append(Person.get_count_of_living_person())

	ax1.clear()
	ax1.plot(PLOT["POPULATION"])

	return 
		

ani = animation.FuncAnimation(fig, main, interval=100)
plt.show()
