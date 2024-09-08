"""
Author: Hamza Bhatti
Module for Homework 5, Problem 1
Object Oriented Programming (50:198:113), Spring 2023

A module to simulate cards and poker hands in a standard deck. 
"""
from random import randint
class Card:
    """
    An instance of the class defines a standard playing card
    with a suit and a face value. 
    """
    allsuits = 'CDHS'
    allfaces = '23456789TJQKA'

    def __init__(self, csuit, cface):
        """
        Initialize the card's suit and face value

        csuit - a character in 'CDHS'
        cface - a character in '23456789TJQKA'
        """
        if csuit not in Card.allsuits or cface not in Card.allfaces:
            raise Exception("Error: Invalid Card object")
        self.suit = csuit
        self.face = cface

    # --------------------------------------------------------
    # COMPLETE THE REST of the Card class implementation below
    # --------------------------------------------------------    

    def __str__(self):
        """
        Returns a string representation of the card in the format "face of suit"
        """
        return self.suit + self.face

    def __eq__(self, other):
        """
        returns True if one card is equal to the other and False otherwise
        """
        return self.face == other.face and self.suit == other.suit

    def __ne__(self, other):
        """
        returns the opposite of __eq__()
        """
        return not self.__eq__(other)

    def __lt__(self, other):
        """
        returns True if one card is less than the other and False otherwise
        """
        if self.suit != other.suit:
            return Card.allsuits.index(self.suit) < Card.allsuits.index(other.suit)
        else:
            return Card.allfaces.index(self.face) < Card.allfaces.index(other.face)

    def __le__(self, other):
        """
        return True if both __lt__() and __eq__() are True
        """
        return self.__lt__(other) or self.__eq__(other)

    def __gt__(self, other):
        """
        returns True if one card is greater than the other and False otherwise
        """
        return not self.__le__(other)

    def __ge__(self, other):
        """
        return True if both __gt__() and __eq__() are True
        """
        return self.__gt__(other) or self.__eq__(other)

class CardDeck:
    """
    A class that represents a deck of cards. The deck starts
    out as a standard 52-card deck but will have fewer cards if
    some cards have been dealt out. 
    """

    # --------------------------------------------------------    
    # COMPLETE the CardDeck class implementation below
    # --------------------------------------------------------
    
    def __init__(self):
        """
        Initializes the instance to the standard 52-card deck
        """
        self.cards = [Card(suit, face) for suit in Card.allsuits for face in Card.allfaces]

    def __len__(self):
        """
        Returns the number of cards in the deck
        """
        return len(self.cards)

    def __str__(self):
        """
        Returns a string that shows all the cards in the deck
        """
        return ', '.join(str(card) for card in self.cards)

    def __iter__(self):
        """
        Returns an iterator object for the deck
        """
        return CardDeckIterator(self.cards)

    def deal(self):
        """
        Returns the top card of the deck. The deck will have one less card after
        this method is called on an instance
        """
        if not self.cards:
            raise ValueError('Deck is empty')
        return self.cards.pop()

    def shuffle(self):
        """
        Randomly shuffles the deck
        """
        for i in range(len(self.cards)-1, 0, -1):
            j = randint(0, i)
            self.cards[i], self.cards[j] = self.cards[j], self.cards[i]

class CardDeckIterator:
    def __init__(self, cards):
        """
        iterator for card deck
        """
        self.cards = cards
        self.index = 0

    def __next__(self):
        """
        iterates over the iterator and raises stop iteration when the index is invalid
        """
        if self.index >= len(self.cards):
            raise StopIteration
        else:
            card = self.cards[self.index]
            self.index +=1
            return card
            
class PokerHand:
    """
    A five card poker hand. The hands in decreasing order of
    rank are 'Straight Flush', 'Four Of A Kind', 'Full House',
    'Flush', 'Straight', 'Three Of A Kind', 'Two Pair', 'One Pair',
    and 'High Card'
    """
    numcards = 5
    handtypes = ['Straight Flush', 'Four Of A Kind',
                 'Full House', 'Flush', 'Straight', 
                 'Three Of A Kind', 'Two Pair', 'One Pair', 
                 'High Card']

    # -------------------------------------------------------------    
    # COMPLETE THE REST of the PokerHand class implementation below
    # -------------------------------------------------------------    

    def __init__(self, deck):
        self.cards = sorted([deck.deal() for _ in range(self.numcards)])
        self.suitcounts = {s: 0 for s in Card.allsuits}
        self.facecounts = {f: 0 for f in Card.allfaces}
        for card in self.cards:
            self.suitcounts[card.suit] += 1
            self.facecounts[card.face] += 1

    def __str__(self):
        """
        Returns a string representation of the poker hand
        """
        return ', '.join(str(card) for card in self.cards)

    def evaluate(self):
        """
        checks for the rankings of the cards
        """
        if self.isStraightFlush():
            return "Straight Flush"
        elif self.isFourOfAKind():
            return "Four of a Kind"
        elif self.isFullHouse():
            return "Full House"
        elif self.isFlush():
            return "Flush"
        elif self.isStraight():
            return "Straight"
        elif self.isThreeOfAKind():
            return "Three of a Kind"
        elif self.isTwoPair():
            return "Two Pair"
        elif self.isOnePair():
            return "One Pair"
        else:
            return "High Card"

    def isStraight(self):
        """
        returns True if the hand has 5 cards with consecutive ranks and False otherwise
        """
        for i in range(len(Card.allfaces) - 4):
            if all(self.facecounts[face] == 1 for face in Card.allfaces[i:i+5]):
                return True
        return False

    def isFlush(self):
        """
        returns True if all cards in the hand have the same suit and False otherwise
        """
        for count in self.suitcounts.values():
            if count == 5:
                return True
        return False

    def isStraightFlush(self):
        """
        returns True if both Straight and Flush are True
        """
        return self.isStraight() and self.isFlush()

    def isThreeOfAKind(self):
        """
        returns True if three of the cards have same face value
        """
        for count in self.facecounts.values():
            if count == 3:
                return True
        return False

    def isFourOfAKind(self):
        """
        returns True if four of the cards have same face value
        """
        for count in self.facecounts.values():
            if count == 4:
                return True
        return False

    def isFullHouse(self):
        """
        returns True if there are 3 cards with same face value and 2 other cards with
        same face value
        """
        return self.isThreeOfAKind() and len(self.facecounts) == 2

    def isTwoPair(self):
        """
        returns True if there are 2 cards with same face value and 2 other cards with
        same face value different from the previous two"""
        
        num_pairs = 0
        for count in self.facecounts.values():
            if count == 2:
                num_pairs += 1
        return num_pairs == 2

    def isOnePair(self):
        """
        returns True if there are 2 cards with same face value and other 3 cards
        different from the previous two and from eachother
        """
        for count in self.facecounts.values():
            if count == 2:
                return True
        return False
    
    
if __name__=="__main__":
    print("---------------------------------------------------")
    print("Testing Program")
    print("This is a pretty basic test code.")
    print("---------------------------------------------------")    
    myDeck = CardDeck()
    print("Standard Deck: "+str(myDeck))
    print("Dealing 5 cards.....")
    hand = PokerHand(myDeck)      # top 5 cards from deck
    print("Sorted Hand: "+str(hand))
    print("Best Rank: %s"%hand.evaluate())

    print("\nA straight flush is no surprise since we didn't shuffle the deck yet!")
    print("We will shuffle the deck once and deal a few more hands....\n")
    myDeck.shuffle()
    print("Shuffled Deck: "+str(myDeck))
    print("")
    
    for i in range(3):
        print("Dealing 5 cards.....")
        hand = PokerHand(myDeck)      # top 5 cards from deck
        print("Sorted Hand: "+str(hand))
        print("Best Rank: %s"%hand.evaluate())
        print("")

    print("Shuffling the deck again....")
    myDeck.shuffle()
    print("Shuffled Deck: "+str(myDeck))
    print("")
    
    for i in range(3):
        print("Dealing 5 cards.....")
        hand = PokerHand(myDeck)      # top 5 cards from deck
        print("Sorted Hand: "+str(hand))
        print("Best Rank: %s"%hand.evaluate())
        print("")
