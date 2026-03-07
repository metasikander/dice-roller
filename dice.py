# coding: utf-8
"""Core dice-rolling logic shared by the CLI and web interfaces."""

import re
import random
import warnings

try:
    # Use the system PRNG if possible
    rng = random.SystemRandom()
except NotImplementedError:
    warnings.warn(
        "A secure pseudo-random number generator is not available "
        "on your system. Falling back to Mersenne Twister."
    )
    rng = random.Random()


def _parse_arithmetic(expression: str) -> int:
    """Evaluate a simple integer arithmetic expression (+, -, *, /) safely."""
    tokens = re.findall(r"-?\d+|[+\-*/]", expression)
    if not tokens:
        raise ValueError(f"Invalid expression: {expression!r}")

    result = int(tokens[0])
    i = 1
    while i < len(tokens):
        op = tokens[i]
        operand = int(tokens[i + 1])
        if op == "+":
            result += operand
        elif op == "-":
            result -= operand
        elif op == "*":
            result *= operand
        elif op == "/":
            if operand == 0:
                raise ZeroDivisionError
            result //= operand
        i += 2
    return result


def dice_roller(input_text: str) -> tuple[int, list[str]]:
    """Roll dice described by input_text and return (total, list of roll strings)."""
    r_dice = re.compile(r"\d*d\d+")
    rolls: list[str] = []

    def roll_dice(match: re.Match) -> str:
        """Roll one dice term and record each individual result."""
        result = 0
        dice_split = match.group(0).split("d")
        times = int(dice_split[0]) if dice_split[0] != "" else 1
        sides = int(dice_split[1])
        for _ in range(times):
            roll = rng.randrange(1, sides + 1)
            rolls.append(f"{roll}/{sides}")
            result += roll
        return str(result)

    substituted = r_dice.sub(roll_dice, input_text)
    total = _parse_arithmetic(substituted)
    return total, rolls


def stats_roll() -> str:
    """Roll 4d6 drop-lowest six times and return formatted results."""
    lines = []
    for _ in range(6):
        total, rolls = dice_roller("4d6")
        lowest = int(min(rolls).split("/")[0])
        lines.append(f"{total - lowest} {rolls}")
    return "\n".join(lines)


def dir_roll() -> str:
    """Pick a random compass direction."""
    directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW", "Stay"]
    return rng.choice(directions)
