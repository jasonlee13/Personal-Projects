import random
import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np
from ps4_classes import BlackJackCard, CardDecks, Busted


class BlackJackHand:
    hit = 'hit'
    stand = 'stand'
    doubledown = 'doubledown'
    #########################

    def __init__(self, deck, initial_bet=1.0):
        """
        Parameters:
        deck - An instance of CardDeck that represents the starting shuffled
               card deck (this deck itself contains one or more standard card decks)
        initial_bet - float, represents the initial bet/wager of the hand
        """
        self.deck = deck #initialize variables
        self.current_bet = initial_bet
        
        cards_dealt = []
        
        for i in range(4): #append four cards to list
            cards_dealt.append(self.deck.deal_card())
            
        self.player = [cards_dealt[0], cards_dealt[2]] #player gets 1st and 3rd cards
        self.dealer = [cards_dealt[1], cards_dealt[3]] #player gets 2nd and 4th cards
        
    def set_bet(self, new_bet):
        """
        Sets the player's current wager in the game.

        Parameters:
        new_bet - the floating point number representing the new wager for the game.
        """
        self.current_bet = new_bet


    def get_bet(self):
        """
        Returns the player's current wager in the game.

        Returns:
        self.current_bet, the floating point number representing the current wager for the game

        """
        return self.current_bet
        

    def set_initial_cards(self, player_cards, dealer_cards):
        """
        Sets the initial cards of the game.
        player_cards - list, containing the inital player cards
        dealer_cards - list, containing the inital dealer cards
        """
        self.player = player_cards[:]
        self.dealer = dealer_cards[:]


    @staticmethod
    def best_value(cards):
        """
        Finds the total value of the cards. All cards must contribute to the
        best sum; however, an Ace may contribute a value of 1 or 11.

        Parameters:
        cards - a list of BlackJackCard instances.

        Returns:
        int, best sum of point values of the cards  
        """
        player = 0
        for card in cards:
            player += card.get_val() #get total value of cards
        
        if player > 21: #if the total value is greater than 21
            for card in cards:
                if card.get_rank() == 'A': #if there is an ace, subtract 10
                    player -= 10
                if player <= 21: #if the score is now less than 21, break
                    break #else go back and see if there is another ace
        
        return player

    def get_player_cards(self):
        """
        Returns:
        list, a copy of the player's cards 
        """
        return self.player.copy()

    def get_dealer_cards(self):
        """
        Returns:
        list, a copy of the dealer's cards 
        """
        return self.dealer.copy()
    
    def get_dealer_upcard(self):
        """
        Returns the dealer's face up card. We define the dealer's face up card
        as the first card in their hand.

        Returns:
        BlackJackCard instance, the dealer's face-up card 
        """
        return self.dealer[0]

    # Strategy 1
    def mimic_dealer_strategy(self):
        """
        A playing strategy in which the player uses the same metric as the
        dealer to determine their next move.

        The player will:
            - hit if the best value of their cards is less than 17
            - stand otherwise

        Returns:
        str, "hit" or "stand" representing the player's decision  
        """
        if BlackJackHand.best_value(self.player) < 17: #if lower than 17, hit; else, stand
            return 'hit'
        else:
            return 'stand'

    # Strategy 2
    def peek_strategy(self):
        """
        A playing strategy in which the player knows the best value of the
        dealer's cards.

        The player will:
            - hit if the best value of their hand is less than that of the dealer's
            - stand otherwise

        Returns:
        str, "hit" or "stand" representing the player's decision
        """
        if BlackJackHand.best_value(self.player) < BlackJackHand.best_value(self.dealer): #if value of player is less than dealer, hit; else, stand
            return 'hit'
        else:
            return 'stand'

    # Strategy 3
    def simple_strategy(self):
        """
        A playing strategy in which the player will
            - stand if one of the following is true:
                - the best value of player's hand is greater than or equal to 17
                - the best value of player's hand is between 12 and 16 (inclusive)
                  AND the dealer's up card is between 2 and 6 (inclusive)  
            - hit otherwise

        Returns:
        str, "hit" or "stand" representing the player's decision 
        """
        if BlackJackHand.best_value(self.player) >= 17: #if the value is greater than 17, stand
            return 'stand'
        elif 12 <= BlackJackHand.best_value(self.player) <= 16 and 2 <= self.get_dealer_upcard().get_val() <= 6: #if between these scores, stand; else, hit
            return 'stand'
        else:
            return 'hit'
        
    # Strategy 4
    def doubledown_strategy(self):
        """
        A playing strategy in which the player will
            - doubledown if the following is true:
                - the best value of the player's cards is 11
            - else they will fall back to using simple_strategy

        Returns:
        str, BlackJackHand.doubledown if player_best_score == 11,
             otherwise the return value of calling simple_strategy to play in the default way
        """
        if BlackJackHand.best_value(self.player) == 11: #if the value is 11, do doubledown; else, do simple strategy
            return BlackJackHand.doubledown
        else:
            return self.simple_strategy()

    def play_player_turn(self, strategy):
        """
        Plays a full round of the player's turn and updates the player's hand
        to include new cards that have been dealt to the player (a hit). The player
        will be dealt a new card until they stand, bust, or doubledown. 
        
        Parameter:
        strategy - function, one of the the 4 playing strategies defined in BlackJackHand
                   (e.g. BlackJackHand.mimic_dealer_strategy, BlackJackHand.double_down_strategy)

        Returns:          
        This function does not return anything.
        """
        strateg = strategy(self)
        while strateg != 'stand': #if strategy is not stand
            if strateg == 'hit': #if it is hit, then append the card
                self.player.append(self.deck.deal_card())
                strateg = strategy(self)
            elif strateg == BlackJackHand.doubledown: #if the strategy is doubledown, make sure to duoble current bet
                self.set_bet(self.current_bet*2)
                self.player.append(self.deck.deal_card())
                strateg = strategy(self)
                break
                
            if BlackJackHand.best_value(self.player) > 21: #score is greater than 21, bust
                raise Busted
                
        if BlackJackHand.best_value(self.player) > 21: #score is greater than 21, bust
            raise Busted

    def play_dealer_turn(self):
        """
        Plays a full round of the dealer's turn and updates the dealer's hand
        to include new cards that have been dealt to the dealer. The dealer
        will get a new card as long as the best value of their hand is less
        than 17. If they go over 21, they bust.
        """
        while BlackJackHand.best_value(self.dealer) < 17: #if the score is less than 17, hit; if greater than 21; bust
            self.dealer.append(self.deck.deal_card())
        if BlackJackHand.best_value(self.dealer) > 21:
            raise Busted

    def __str__(self):
        """
        Returns:
        str, representation of the player and dealer and dealer hands.
        """
        result = 'Player: '
        for c in self.player:
            result += str(c) + ','
        result = result[:-1] + '    '
        result += '\n   Dealer '
        for c in self.dealer:
            result += str(c) + ','
        return result[:-1]


def play_hand(deck, strategy, initial_bet=1.0):
    """
    Plays a hand of Blackjack and determines the amount of money the player
    gets back based on the bet/wager of the hand.

    Parameters:
        deck - an instance of CardDeck
        strategy - function, one of the the four playing strategies defined in BlackJackHand
                   (e.g. BlackJackHand.mimic_dealer_strategy)
        initial_bet - float, the amount that the player initially bets (default=1.0)

    Returns:
        tuple (float, float): (amount_wagered, amount_won)
    """
    
    game = BlackJackHand(deck, initial_bet)
    if BlackJackHand.best_value(game.get_player_cards()) == 21 and BlackJackHand.best_value(game.get_dealer_cards()) != 21:
        return (game.get_bet(), game.get_bet()*2.5) #2.5 bet if player gets blackjack and dealer does not
    elif BlackJackHand.best_value(game.get_player_cards()) == 21 and BlackJackHand.best_value(game.get_dealer_cards()) == 21:
        return (game.get_bet(), game.get_bet()) #if tied, return same bet
    elif BlackJackHand.best_value(game.get_player_cards()) != 21 and BlackJackHand.best_value(game.get_dealer_cards()) == 21:
        return (game.get_bet(), 0) #if dealer gets blackjack and player does not, return 0
    
    try:
        game.play_player_turn(strategy) #try strategy; if bust, then return 0
    except Busted:
        return (game.get_bet(), 0)
    
    try:
        game.play_dealer_turn() #try strategy; if bust, then return win
    except Busted:
        return (game.get_bet(), game.get_bet()*2)
    
    if BlackJackHand.best_value(game.get_player_cards()) == BlackJackHand.best_value(game.get_dealer_cards()):
        return (game.get_bet(), game.get_bet()) #if they are tied, then return same
    elif BlackJackHand.best_value(game.get_player_cards()) < BlackJackHand.best_value(game.get_dealer_cards()):
        return (game.get_bet(), 0) #if player is less, then return 0
    elif BlackJackHand.best_value(game.get_player_cards()) > BlackJackHand.best_value(game.get_dealer_cards()):
        return (game.get_bet(), game.get_bet()*2) #if player is more, then return win
   
    

def run_simulation(strategy, initial_bet=2.0, num_decks=8, num_hands=20, num_trials=2000, show_plot=False):
    """
    Runs a simulation and generates a normal distribution reflecting 
    the distribution of player's rates of return across all trials

    Parameters:

        strategy - function, one of the the four playing strategies defined in BlackJackHand
                   (e.g. BlackJackHand.mimic_dealer_strategy)
        initial_bet - float, the amount that the player initially bets each hand. (default=2)
        num_decks - int, the number of standard card decks in the CardDeck. (default=8)
        num_hands - int, the number of hands the player plays in each trial. (default=20)
        num_trials - int, the total number of trials in the simulation. (default=100)
        show_plot - bool, True if the plot should be displayed, False otherwise. (default=False)

    Returns:

        tuple, containing the following 3 elements:
            - list of the player's rate of return for each trial
            - float, the average rate of return across all the trials
            - float, the standard deviation of rates of return across all trials
    """
    result = []
    for i in range(num_trials): #for every trial
        total = 0 #initialize new variables
        total_bet = 0
        game = CardDecks(num_decks, BlackJackCard)
        for j in range(num_hands): #play game
            bet, win = play_hand(game, strategy, initial_bet)
            total_bet += bet #calculate total bet
            total += win #calculate total win
        rate_of_return = 100*(total-total_bet)/(total_bet) #calculate rate of return
        result.append(rate_of_return)

    average = np.mean(result) #mean of all the results of every trial
    st_dev = np.std(result) #st_dev of all the results of every trial

    if show_plot:
        plt.title('Player ROI on Playing ' + str(num_hands) + ' Hands' + ' (' + str(strategy.__name__) + ') \n' + '(Mean = ' + str(average) + '%, SD = ' + str(st_dev) + '%)')
        plt.xlabel('% Return')
        
        result.sort()
        y_values = stats.norm.pdf(result, average, st_dev) #plot normal curve
        plt.plot(result, y_values) #plot the x and y values
        plt.hist(result, density = True)
        plt.show()
    
    return (result, average, st_dev)
            

# if __name__ == '__main__':
    #
    # You can uncomment pieces of the following to test each strategy separately.
    #
    # Default plots:
    #
#    run_simulation(BlackJackHand.mimic_dealer_strategy, show_plot=True)
#    run_simulation(BlackJackHand.peek_strategy, show_plot=True)
#    run_simulation(BlackJackHand.simple_strategy, show_plot=True)
#    run_simulation(BlackJackHand.doubledown_strategy, show_plot=True)
#
# Uncomment to run all simulations:
# #
#     run_all_simulations([BlackJackHand.mimic_dealer_strategy,
#                          BlackJackHand.peek_strategy,
#                          BlackJackHand.simple_strategy,
#                          BlackJackHand.doubledown_strategy])

# Copies of the student tester simulations are below to aid in debugging.
#
# Make sure you include the following line to use same random number generator as the tester!
#    random.seed(0)
#
#   Simulation used in test_29_run_simulation_mimic_dealer_strategy
#    run_simulation(BlackJackHand.mimic_dealer_strategy,
#                   initial_bet=2, num_decks=8, num_hands=20, num_trials=4000, show_plot=True)
#
#   Simulation used in test_30_run_simulation_peek_strategy
#    run_simulation(BlackJackHand.peek_strategy,
#                   initial_bet=2, num_decks=8, num_hands=20, num_trials=4000, show_plot=True)
#
#   Simulation used in test_31_run_simulation_simple_strategy
#    run_simulation(BlackJackHand.simple_strategy,
#                   initial_bet=2, num_decks=8, num_hands=20, num_trials=4000, show_plot=True)
#
#   Simulation used in test_32_run_simulation_double_down_strategy
#    run_simulation(BlackJackHand.doubledown_strategy,
#                   initial_bet=2, num_decks=8, num_hands=20, num_trials=4000, show_plot=True)
#
#   Use the following pass if you have no __main__ code enabled.
    pass
