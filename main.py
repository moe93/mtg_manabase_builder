'''
*
* Manabase calculator to ensure you have the "correct color"
* land drop each turn for a 60 cards deck...also avoid
* getting mana flooded/fucked, that ain't cool
*
* VERSION: 0.01a
*   - ADDED   : Hi!
*
*
* KNOWN ISSUES:
*   - Nada atm.
*
*
* AUTHOR                    :   Mohammad Odeh
* DATE                      :   Apr. 26th, 2019 Year of the COVID
* LAST CONTRIBUTION DATE    :   ---
*
'''

from    time                    import  sleep, time             # Timers/delays
from    platform                import  system                  # Running platform info
from    datetime                import  datetime                # Get date and time

    
from    argparse                import  ArgumentParser          # Add input arguments to script
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
ap.add_argument( "-nl", "--non_land" , type = int    ,
                 dest   = "non_land" , default =  0  ,
                 help   = "{}".format(string)           )

# Total number of 1 mana cards
string = "Total 1 mana cards"
ap.add_argument( "-m1", "--mana_1" , type = int    ,
                 dest   = "mana_1" , default =  0  ,
                 help   = "{}".format(string)           )

# Total number of 2 mana cards
string = "Total 2 mana cards"
ap.add_argument( "-m2", "--mana_2" , type = int    ,
                 dest   = "mana_2" , default =  0  ,
                 help   = "{}".format(string)           )

# Total number of 3 mana cards
string = "Total 3 mana cards"
ap.add_argument( "-m3", "--mana_3" , type = int    ,
                 dest   = "mana_3" , default =  0  ,
                 help   = "{}".format(string)           )

# Total number of 4 mana cards
string = "Total 4 mana cards"
ap.add_argument( "-m1", "--mana_4" , type = int    ,
                 dest   = "mana_4" , default =  0  ,
                 help   = "{}".format(string)           )

# Total number of 5 mana cards
string = "Total 5 mana cards"
ap.add_argument( "-m1", "--mana_5" , type = int    ,
                 dest   = "mana_5" , default =  0  ,
                 help   = "{}".format(string)           )

# Total number of 6+ mana cards
string = "Total 6+ mana cards"
ap.add_argument( "-m6p", "--mana_6p", type = int    ,
                 dest   = "mana_6p" , default =  0  ,
                 help   = "{}".format(string)           )

args = ap.parse_args()

args.dev_mode       = True
if( args.dev_mode ):
    args.non_land   = 35

# ************************************************************************
# ===========================> PROGRAM  SETUP <==========================*
# ************************************************************************

class MTG_mana( object ):

    def __init__( self ):
        if( args.non_land == 0 ):                                       # Make sure the deck has cards to begin with
            raise ValueError( "Deck can't have 0 cards!" )              # ...

        self.compute_curve()                                            # Compute the mana curve
        self.compute_mana()                                             # Compute how many lands are needed

# --------------------------

    def compute_curve( self ):
        '''
        Compute the current curve of the deck and plot
        '''

        
# --------------------------

    def compute_mana( self ):
        '''
        Compute mana requirements

        NOTE:
            - Doesn't take into consideration mana-fixing cards
        '''
        
                

# ************************************************************************
# =========================> MAKE IT ALL HAPPEN <=========================
# ************************************************************************

prog = MTG_mana()                                                         # Gimme dem mana recommendations
