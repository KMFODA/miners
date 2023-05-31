# The MIT License (MIT)
# Copyright © 2023 Yuma Rao

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the “Software”), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import wandb
import bittensor as bt
from typing import List, Dict, Union, Tuple, Callable

def blacklist( self, func: Callable, forward_call: "bt.TextPromptingForwardCall" ) -> Union[ Tuple[bool, str], bool ]:
    bt.logging.trace( 'run blacklist function')

    # First check to see if the black list function is ovveridden by the subclass.
    try: 
        return func(forward_call)
    
    except NotImplementedError:
        # The subclass did not override the blacklist function.
        pass

    except Exception as e:
        # There was an error in their blacklist function.
        bt.logging.error( f'Error in blacklist function: {e}') 

    def run_checks():
        # Check if we allow non-registered users
        # If we do, all messages go through.
        if self.config.miner.blacklist.allow_non_registered:
            return False, 'allow all non-registered hotkeys.'

        # Check if the key is white listed.
        if forward_call.src_hotkey in self.config.miner.blacklist.whitelist:
            return False, 'whitelisted hotkey'

        # Check if the key is black listed.
        if forward_call.src_hotkey in self.config.miner.blacklist.blacklist:
            return True, 'blacklisted hotkey'

        # Check if the key is registered.
        registered = False
        if self.metagraph is not None:
            registered = forward_call.src_hotkey in self.metagraph.hotkeys

        # Check if we allow non-registered users.
        if not registered:
            return True, 'hotkey not registered'

        # If the user is registered, it has a UID.
        uid = self.metagraph.hotkeys.index( forward_call.src_hotkey )

        # Check if the key has validator permit
        if self.metagraph.validator_permit[uid] and self.config.miner.blacklist.force_validator_permit:
            return True, 'validator permit required'

        # Get the uid stake amount.
        stake_amount = self.metagraph.S[uid].item() 

        # Check if the user has enough stake.
        if stake_amount < self.config.miner.minimum_stake_requirementc:
            return True, 'hotkey does not have enough stake'

        # Other wise the user is not blacklisted.
        return False, 'passed blacklist'
        
    # Run checks.
    does_blacklist, reason = run_checks()

    # Log blacklist event.
    bt.logging.trace( f'blacklisted: {does_blacklist}, reason: {reason}' )
    if self.config.wandb.on: wandb.log( { 'blacklisted': int( does_blacklist ), 'Reason': reason, 'hotkey': forward_call.src_hotkey } )

    # Return.
    return does_blacklist, reason
