'''
*
* Manabase calculator to ensure you have the "correct color"
* land drop each turn for a 60 cards deck...also avoid
* getting mana flooded/fucked, that ain't cool
*
* VERSION: 0.05a
*   - ADDED   : Hi!
*   - ADDED   : Mana curve plot
*   - ADDED   : Deck generator
*
*
* KNOWN ISSUES:
*   - Nada atm.
*
*
* AUTHOR                    :   Mohammad Odeh
* DATE                      :   Apr. 26th, 2020 Year of the COVID
* LAST CONTRIBUTION DATE    :   Apr. 28th, 2020 Year of the COVID
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
        self.make_deck()                                                # Create a deck and shuffle it
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
            [num, cmc] = args.cmc_color[i].split('x')                   # Extract #cards, cmc

            for j in range( 0, int(num) ):                              # Append that many # of cards
                self.deck.append( cmc )                                 # of specifc cmc to deck

        if( len(self.deck) != args.non_land ):                          # Make sure card numbers match
            raise ValueError( "Card totals do NOT match!" )             # ...


        # Generate lands, for now use 1xLand for 2xColor
        self.land_cards = list()                                        # Create empty lands deck (temp)
        
        for i in range( 0, len(args.mana_color) ):
            # FROM: https://stackoverflow.com/questions/46418265/how-to-count-the-number-of-times-a-specific-character-appears-in-a-list
            total_mana = sum( s.count(args.mana_color[i]) for s in self.deck )

            for j in range( 0, -(-total_mana//2) ):                     # -(-x//y) rounds up
                self.land_cards.append( args.mana_color[i]+'L' )        # Generate list of lands


        # Now shuffle deck of cards + lands
        seed( time() )                                                  # Plant seed for random number generator
        self.deck.extend( self.land_cards )                             # Add lands to main deck
        shuffle( self.deck )                                            # Shuffle deck

        if( args.dev_mode ): print( self.deck )                         # Print

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
### --------------------------
##
##    def draw_card( self ):
##        '''
##        Draw 1 card
##        '''
##

# ************************************************************************
# =========================> MAKE IT ALL HAPPEN <=========================
# ************************************************************************

prog = MTG_mana()                                                       # Gimme dem mana recommendations
