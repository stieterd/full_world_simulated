# full_world_simulated

 - Please understand that this was a very ambitious project, and it isnt even close to being finished. It has a lot of bugs and a lot of it is unfinished.
 

*******************************************************************************CREATURES*******************************************************************************
- if edible in radius of 50px:
	 creature runs to it if hunger is above {certain number written in creature dna}

- hunger will increase every {in dna written time} with 1

- else if edible not in radius but creature is hungry:
	creature goes into a direction randomly and only changes from direction if they didnt find any food for more then 5 seconds.

- if hunger is not above {certain number written in creature dna}:

	creature wanders around and will be able to fall in love with other creatures within radius 100px



there is an allel for falling in love, and an allel for attracting other creatures. If the allel for attracting creatures is close enough to the allel of falling in love creatures
can fall in love with each other and get kids.

there is a predator allel, this allel will make creatures being able to eat other creatures.


*******************************************************************************PLANTS*******************************************************************************

Plants also have dna, dna for growth, reproduction etcetera

There is also a sun that rises every day at specific place, and goes down at a specific place too, the sun almost feeds all the tiles inside the border. Some tiles are better
influenced by the sun then others

There is rain too, this rain is completely random and will occure on random tiles. This rain will feed the plants, without the rain plants will starve. Starvation is also an allel
inside the dna

plants reproduce when fully grown at day time. When reproducing it chooses complete random tiles to place his children inside a radius of 300px, reproduction is probably also a
property inside the dna. To let the babyplants grow the tile has to be wet enough and have enough sun. Otherwise the babyplants will never grow


*******************************************************************************DNA AND BEHAVIOUR*******************************************************************************

DNA contains only 1's and zeros, 1 is dominant, 0 is recessive.

parents will give their dna to their child when getting the child. The Dna of a creature contains two arrays(DNA strings) plants have only one. Because it takes only 1 plant to reproduce.
when parents give dna to their kids mutation occures.

Behaviour are offsets that will change the dna a little(NOT everything, only a few things, like finding out the radius of edible).
Behaviour will start at 0 at every child. When the children are growing the behaviour will mutate a little. It will only mutate if the creature is struggling, for example: starving.

*******************************************************************************WEATHER*******************************************************************************

The area within the borders will be divided in +/- 50*50 tiles. These tiles will contain information that will concern every pixel inside the tile.

Information on a tile:

	- how wet is the tile(0-100)
	- how much sunlight does it get per day(0-100)

Sunlight is going to influence a lot. The amount of sunlight and rain a tile is given, tells how much energy the plant on this tile contains. So if a plant grows on a tile with no
sunlight and no rain. The creature that will eat the plant will still be hungry. Because the plant didnt contain enough energy to give to the creature.

