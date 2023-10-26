def get_guild_exp_data(exp):
    """
    The function `get_guild_exp_data` calculates the guild level, remaining experience, and total
    experience based on the given experience points.
    
    @param exp The "exp" parameter represents the amount of experience points that a guild has.
    
    @return The function `get_guild_exp_data` returns a tuple containing the following values:
    """
    EXP_NEEDED = [
        100000,
        150000,
        250000,
        500000,
        750000,
        1000000,
        1250000,
        1500000,
        2000000,
        2500000,
        2500000,
        2500000,
        2500000,
        2500000,
        3000000,
    ]

    level = 0
    total_exp = 0  # Initialize total experience points

    for i in range(1001):
        if i >= len(EXP_NEEDED):
            need = EXP_NEEDED[-1]
        else:
            need = EXP_NEEDED[i]

        if exp - need < 0:
            exp_needed = need
            exp_remaining = need - exp
            guild_level = round((level + exp / need), 2)
            total_exp += exp  # Accumulate total experience points
            return guild_level, exp, exp_needed, exp_remaining, total_exp
        level += 1
        total_exp += need  # Accumulate total experience points
        exp -= need

    return 1000, 0, 0, 0, total_exp  # Level cap and default values if not found