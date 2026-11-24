def pl_true(sentence, model):
    return eval(sentence, {}, model)


def tt_check_all(KB, alpha, symbols, model):

    if len(symbols) == 0:
        if pl_true(KB, model):
            return pl_true(alpha, model)
        else:
            return True

    P = symbols[0]
    rest = symbols[1:]

    return (
        tt_check_all(KB, alpha, rest, {**model, P: True})
        and
        tt_check_all(KB, alpha, rest, {**model, P: False})
    )


def tt_entails(KB, alpha, symbols):
    return tt_check_all(KB, alpha, symbols, {})


# User input
KB = input("Enter Knowledge Base (use and, or, not): ")
alpha = input("Enter Query: ")

# Enter proposition symbols
symbols = input("Enter proposition symbols separated by space: ").split()

# Check entailment
if tt_entails(KB, alpha, symbols):
    print("KB entails the Query (TRUE)")
else:
    print("KB does not entail the Query (FALSE)")