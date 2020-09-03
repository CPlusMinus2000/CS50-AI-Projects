from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(And(AKnight, AKnave), AKnave),
    Not(And(And(AKnight, AKnave), AKnave))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    Or(And(AKnave, BKnave), AKnave),
    Not(And(And(AKnave, BKnave), AKnave))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    Or(Biconditional(AKnight, BKnight), AKnave),
    Not(And(Biconditional(AKnight, BKnight), AKnave)),
    Or(Biconditional(AKnight, BKnave), BKnave),
    Not(And(Biconditional(AKnight, BKnave), BKnave))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave)),
    Or(
        And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
        And(Or(AKnave, AKnave), Not(And(AKnave, AKnave)))
    ),
    Not(And(
        And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
        And(Or(AKnave, AKnave), Not(And(AKnave, AKnave)))
    )),
    Or(And(Or(AKnave, AKnave), Not(And(AKnave, AKnave))), BKnave),
    Not(And(And(Or(AKnave, AKnave), Not(And(AKnave, AKnave))), BKnave)),
    Or(CKnave, BKnave),
    Not(And(CKnave, BKnave)),
    Or(AKnight, CKnave),
    Not(And(AKnight, CKnave))
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
