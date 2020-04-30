'''
*
* Manabase calculator to ensure you have the "correct color"
* land drop each turn for a 60 cards deck...also avoid
* getting mana flooded/fucked, that ain't cool
*
* VERSION: 0.07a
*   - ADDED   : Hi!
*   - ADDED   : Mana curve plot
*   - ADDED   : Deck generator
*   - ADDED   : Hand + card draw (by extension, a 7 card starting hand)
*   - ADDED   : Implement mulligan rule
*
*
* KNOWN ISSUES:
*   - Nada atm.
*
*
* AUTHOR                    :   Mohammad Odeh
* DATE                      :   Apr. 26th, 2020 Year of the COVID
* LAST CONTRIBUTION DATE    :   Apr. 30th, 2020 Year of the COVID
*
'''

from    time                    import  sleep, time             # Timers/delays
from    platform                import  system                  # Running platform info
from    datetime                import  datetime                # Get date and time
import  matplotlib.pyplot       as      plt                     # Plot stuff

from    random                  import  seed, shuffle           # Go entropy!
    
from    argparse                import  ArgumentParser          # Add input arguments to script
from    scipy                   import  interpolate             # Interpolate points for nice plots
import  numpy                   as      np                      # Fast array creation
import  os                                                      # Dir/path manipulation

# ************************************************************************
# =====================> CONSTRUCT ARGUMENT PARSER <=====================*
# ************************************************************************

ap = ArgumentParser()

# Developer mode, makes life easy for me
string = "Enter developer mode"
ap.add_argument( "--dev-mode"           ,
                 dest   = "dev_mode"    ,
                 action = 'store_true'  , default=False ,
                 help   = "{}".format(string)           )

# Total number of non-land cards
string = "Total non-land cards"
ap.add_argument( "-nl", "--non_land" , type = int   ,
                 dest   = "non_land" , default =  0 ,
                 help   = "{}".format(string)       )

# This is the correct way to handle accepting multiple arguments.
# '+' == 1 or more.
# '*' == 0 or more.
# '?' == 0 or 1.
# FROM: https://stackoverflow.com/questions/15753701/how-can-i-pass-a-list-as-a-command-line-argument-with-argparse
# Number of cards with CMC 1, 2,..., 6+
string = "Number of cards with CMC 1, 2,..., 6+"
ap.add_argument( "-cmc", nargs='+'  , type=int  ,
                 dest   = "cmc", default = 0    ,
                 help   = "{}".format(string)   )


# Number of cards with the same colored CMC
# i.e 3x Brineborn Cutthroat + 3x Negate == 6x1U"
string = "Total number of cards with same coloed CMC."
string = string + "\ni.e 3x Brineborn Cutthroat + 3x Negate == 6x1U"
string = string + "\ni.e 3x Ashiok + 4x Slitherswisp == 7xUBB"
ap.add_argument( "--cmc_color", nargs='+'  , 
                 dest   = "cmc_color"      ,
                 help   = "{}".format(string)       )

# Mana colors this deck plays
string = "Manabase colors this deck plays."
string = string + "\ni.e Black == B, blue == U, white == W, etc..."
ap.add_argument( "--mana_color", nargs='+'  ,
                 dest   = "mana_color"      ,
                 help   = "{}".format(string)       )

args = ap.parse_args()

args.dev_mode       = True
if( args.dev_mode ):
    args.non_land   = 35
    args.cmc        = [3, 17, 10, 3, 0, 2]
    args.cmc_color  = [ "3xU", "11x1U", "9x1B", "3x2U", "4xUBB", "3x2UU", "2x4UB" ]
    args.mana_color = [ "B", "U" ]

# ************************************************************************
# ===========================> PROGRAM  SETUP <==========================*
# ************************************************************************

class MTG_mana( object ):

    def __init__( self ):
        if( args.non_land == 0 ):                                       # Make sure the deck has cards to begin with
            raise ValueError( "Deck can't have 0 cards!" )              # ...

        if( sum(args.cmc) != args.non_land ):                           # Make sure total card numbers match
            raise ValueError( "Card totals do NOT match!" )             # ...

##        self.compute_curve()                                            # Compute the mana curve

        self.hand = list()                                              # Create an empty hand variable
        self.mulligan_attempts = 0                                      # How many times we mulliganed
        
        self.make_deck()                                                # Create a deck and shuffle it
        self.draw_card( init=True )                                     # Draw starting hand

##        self.play_turn()                                                # Play a land and a card (if possible)
        
##        self.compute_mana()                                             # Compute how many lands are needed

# --------------------------

    def compute_curve( self ):
        '''
        Compute the current curve of the deck and plot
        '''

        # Assign data to variables
        x = np.linspace( 1, 6, 6 )
        y = np.array( args.cmc )

        # Interpolate
        x_interp = np.linspace( x.min(), x.max(), 500 )
        f = interpolate.interp1d(x, y, kind='cubic')

        # Apply interpolater to dataset
        y_interp = f( x_interp )

        # Create plot
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1, facecolor="1.0")

        # Set xy-axes scale + labels
        ax.set_xlim( [0, 6] )
        ax.set_ylim( [0, 25] )
        ax.set_xlabel( 'CMC' )
        ax.set_ylabel( '# of Cards' )
    
        plt.plot( x_interp, y_interp ); plt.scatter (x, y)              # Plot curve; plot points
                                                              
        ax.grid( which='both' )                                         # Add a grid                               
        ax.grid( which='minor', alpha=0.2 )                             # Modify transperancy...
        ax.grid( which='major', alpha=0.5 )                             # ...settings for the grids

        plt.ion(); plt.show()                                           # Non-blocking plot
        
# --------------------------

    def make_deck( self ):
        '''
        Make a 60 cards deck
        '''

        # Prepare cards deck
        self.deck = list()                                              # Make empty deck
        for i in range( 0, len(args.cmc_color) ):                       # Loop over args.cmc_color
            [num, cmc] = args.cmc_color[i].split('x')                   #   Extract #cards, cmc

            for j in range( 0, int(num) ):                              #   Append that many # of cards
                self.deck.append( cmc )                                 #   of specifc cmc to deck

        if( len(self.deck) != args.non_land ):                          # Make sure card numbers match
            raise ValueError( "Card totals do NOT match!" )             # ...


        # Generate lands, for now use 1xLand for 2xColor
        self.land_cards = list()                                        # Create empty lands deck (temp)
        
        for i in range( 0, len(args.mana_color) ):                      # Find out land color requirements from input
            # FROM: https://stackoverflow.com/questions/46418265/how-to-count-the-number-of-times-a-specific-character-appears-in-a-list
            total_mana = sum( s.count(args.mana_color[i]) for s in self.deck )

            for j in range( 0, -(-total_mana//2) ):                     # -(-x//y) rounds up
                self.land_cards.append( args.mana_color[i]+'L' )        #   Generate list of lands


        # Now shuffle deck of cards + lands
        seed( time() )                                                  # Plant seed for random number generator
        self.deck.extend( self.land_cards )                             # Add lands to main deck
        shuffle( self.deck )                                            # Shuffle deck

        if( args.dev_mode ): print( self.deck )                         # [INFO] Print deck

# --------------------------

    def draw_card( self, init=False ):
        '''
        Draw 1 card

        NOTE:
            - if( init==True ): draw 7 cards
        '''

        if( init ):                                                     # If initial draw
            for i in range( 0, 7-self.mulligan_attempts ):              #   Draw (7-mulligan_attempts) cards
                self.hand.append( self.deck.pop() )                     #       Pop first card from deck into hand
            if( args.dev_mode ): print( self.hand )                     # [INFO] Print hand
            
            num_lands = sum( s.count('L') for s in self.hand )          # Check hand for # of lands
            if( num_lands == len(self.hand)-2 or num_lands < 2 ):       # If too many\few lands, mulligan
                self.mulligan()                                         #   Mulligan
                
        else:                                                           # Else
            self.hand.append( self.deck.pop() )                         #   Draw 1 card

# --------------------------

    def mulligan( self ):
        '''
        Return hand to deck, shuffle, then draw one less card
        '''

        self.deck.extend( self.hand )                                   # Return hand to deck
        self.hand.clear()                                               # Clear hand
        shuffle( self.deck )                                            # Shuffle deck once more

        self.mulligan_attempts += 1                                     # One less card in starting hand
        if( args.dev_mode ): print( "[INFO] Mulliganing {}".format(self.mulligan_attempts) )         # [INFO] ...
        
        if( self.mulligan_attempts == 7 ):                              # Check if we exceeded number of mulligan attempts
            print( "Maximum mulligan attempts reached. Quitting!" )     #   [INFO] ...
            quit()                                                      #   Quit program
            
        else:                                                           # If not
            self.draw_card( init=True )                                 #   Draw hand with (mulligan_attempts) less cards

### --------------------------
##
##    def play_turn( self ):
##        '''
##        1. Check hand for lands
##        2. Determine # of cards in hand with
##            CMC that are playable this turn.
##        3. Play land card if possible
##        4. Else
##        '''
##
##        quit()
            
### --------------------------
##
##    def compute_mana( self ):
##        '''
##        Compute mana requirements
##
##        NOTE:
##            - Doesn't take into consideration mana-fixing cards
##        '''
##

# ************************************************************************
# =========================> MAKE IT ALL HAPPEN <=========================
# ************************************************************************

prog = MTG_mana()                                                       # Gimme dem mana recommendations
