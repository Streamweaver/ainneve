"""
Economy module.
"""
from evennia.utils.dbserialize import _SaverDict

import locale

class InsufficientFunds(ValueError):
    """Represents an error in a financial transaction."""
    pass



def transfer_funds(src, dst, credits):
    """Transfers a given value from src from dst.

    Args:
        src:  Any object with a db.credit property
        dst:  Any object with a db.credit property
        credits (int): Amount of credits to transfer.

    Note:
        If either 'src' or 'dst' are None, the money is created
        or destroyed by this function.
    """
    src_val = src.db.credits if src else 0
    dst_val = dst.db.credits if dst else 0
    # check there's enough
    if src is not None and src_val < credits:
        raise InsufficientFunds("Insufficient funds.")

    if src is not None:
        src.db.credits = src_val - credits

    if dst is not None:
        dst.db.credits = dst_val + credits


def format_credits(credits):
    """Returns a string representing a value as numbers of coins."""
    locale.setlocale(locale.LC_ALL, 'en_US')
    locale.format("%d", credits, grouping=True)
    output = "|w{}|n cr. ".format(locale.format("%d", credits, grouping=True))
    return output.strip()
