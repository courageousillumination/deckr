#deckr

1. [Overview](#overview)
2. [Setup](#setup)
3. [Writing a Game](#writing-a-game)
4. [Playing a Game](#playing-a-game) 
5. [What is Implemented](#what-is-implemented)
6. [FAQ](#faq)

## Overview

Deckr is a card game engine for [CMSC 22001](http://people.cs.uchicago.edu/~shanlu/teaching/22001_fa14/): Software Construction. The goal of this project is to create a reusable and extendable system for playing card games. Our system allows a user to define a card game using a combination of simple scripting and card definitions. Ideally our system will support many different types of card games from simple playing card games (Go Fish, War, Hearts) to complex trading card games (Magic: The Gathering, Pokemon, Yu-Gi-Oh!)

This application currently offers 3 games: Solitaire, Hearts, and Dominion.

## Setup

#### Prerequisites

To set up deckr you must have python 2.7, virtualenv, pip, and libevent. All of
these can be installed using your favorite package manager. If you are running Mac OSX and do not have Xcode installed, you will need to install it. You may need to use sudo when running pip install.

#### Installation

First clone the repository:
```
 git clone https://github.com/courageousillumination/deckr.git
```

After cloning the repository run the following commands:
```
  cd deckr
  virtualenv venv
  source venv/bin/activate
  pip install -r requirements.txt
  cd webapp
  make setup
  make run
```

At this point the server should be up and running at localhost:8000.

The webapp also includes a Makefile that makes some general tasks easier.
* `make test` will run the unit tests
* `make verify` will run unit tests, integration tests, and compile coverage information (all data will be written into a reports directory)
* `make lint` will run pylint on the code base and generate a report.
* `make autolint` will run autopep8 on the deckr code base to reduce pep8 violations.


## Writing a Game

Check out [Writing a Game Guide](https://github.com/courageousillumination/deckr/blob/documentation/docs/game_tutorial.md) for an intro to creating a game definition that can be uploaded to Deckr.

## Playing a Game

Check out [Playing a Game](https://github.com/courageousillumination/deckr/blob/documentation/docs/playing_a_game.md) for instructions and other information on how to play a game. Also feel free to check out our [Acceptance Tests](https://github.com/courageousillumination/deckr/blob/documentation/docs/acceptance_tests.md) if you're interested in doing some testing!

## What is Implemented

Check out [What is Implemented](https://github.com/courageousillumination/deckr/blob/documentation/docs/what_is_implemented.md) to see a summary of what we implemented during the first and second iterations.

## FAQ

Check out the [FAQ](https://github.com/courageousillumination/deckr/blob/documentation/docs/faq.md) to get answers to frequently asked questions, and to see a list of known issues.
