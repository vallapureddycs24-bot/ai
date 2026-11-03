def is_variable(x):
    # Lowercase strings are treated as variables (e.g., 'x', 'y')
    return isinstance(x, str) and len(x) > 0 and x.islower()


def is_constant(x):
    # Uppercase strings or numbers are treated as constants (e.g., 'A', 5)
    return isinstance(x, (int, float)) or (isinstance(x, str) and len(x) > 0 and (x.isupper() or x.isdigit()))


def occurs_in(var, expr):
    # Check if a variable occurs inside a compound expression
    if var == expr:
        return True
    if isinstance(expr, list):
        return any(occurs_in(var, arg) for arg in expr)
    return False


def apply_substitution(subst, expr):
    # Apply a list of substitutions to an expression
    if not subst or subst == "NIL":
        return expr
    if is_variable(expr):
        for s in subst:
            if expr in s:
                return apply_substitution(subst, s[expr])
        return expr
    if isinstance(expr, list):
        return [apply_substitution(subst, element) for element in expr]
    return expr


def unify(psi1, psi2):
    # Step 1: Variable or Constant checks
    if is_variable(psi1) or is_constant(psi1) or is_variable(psi2) or is_constant(psi2):
        if psi1 == psi2:
            return "NIL"
        elif is_variable(psi1):
            if occurs_in(psi1, psi2):
                return "FAILURE"
            return [{psi1: psi2}]
        elif is_variable(psi2):
            if occurs_in(psi2, psi1):
                return "FAILURE"
            return [{psi2: psi1}]
        else:
            return "FAILURE"

    # Step 2: Check predicate symbols
    if psi1[0] != psi2[0]:
        return "FAILURE"

    # Step 3: Check number of arguments
    if len(psi1) != len(psi2):
        return "FAILURE"

    # Step 4: Initialize substitution set
    subst = "NIL"

    # Step 5: Unify arguments element-by-element
    for i in range(1, len(psi1)):
        s = unify(psi1[i], psi2[i])
        
        if s == "FAILURE":
            return "FAILURE"
            
        if s != "NIL":
            if subst == "NIL":
                subst = []
            
            subst = s + subst
            
            # Apply substitution to remaining items
            for j in range(i + 1, len(psi1)):
                psi1[j] = apply_substitution(s, psi1[j])
                psi2[j] = apply_substitution(s, psi2[j])

    # Step 6: Return final substitution list
    return subst


# --- Normal Example Usage ---
# Unifying P(x, B) and P(A, y)
expression1 = ["P", "x", "B"]
expression2 = ["P", "A", "y"]

result = unify(expression1, expression2)
print("Substitution Set:", result)
