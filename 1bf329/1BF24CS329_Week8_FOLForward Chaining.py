import itertools

var_counter = itertools.count(1)


def is_variable(term):
    """Variables start with lowercase; constants start with uppercase."""
    return isinstance(term, str) and term.islower()


def substitute(theta, expr):
    """Applies substitution dictionary theta to an expression."""
    if theta is None:
        return None
    if isinstance(expr, str):
        while expr in theta:
            expr = theta[expr]
        return expr
    elif isinstance(expr, tuple):
        return tuple(substitute(theta, item) for item in expr)
    elif isinstance(expr, list):
        return [substitute(theta, item) for item in expr]
    return expr


def occur_check(var, x, theta):
    if var == x:
        return True
    elif is_variable(x) and x in theta:
        return occur_check(var, theta[x], theta)
    elif isinstance(x, tuple):
        return any(occur_check(var, item, theta) for item in x)
    return False


def unify_var(var, x, theta):
    if var in theta:
        return unify(theta[var], x, theta)
    elif is_variable(x) and x in theta:
        return unify(var, theta[x], theta)
    elif occur_check(var, x, theta):
        return None
    else:
        new_theta = theta.copy()
        new_theta[var] = x
        return new_theta


def unify(x, y, theta=None):
    """UNIFY(x, y): Returns substitution making x and y identical, or None."""
    if theta is None:
        theta = {}
    if x == y:
        return theta
    elif is_variable(x):
        return unify_var(x, y, theta)
    elif is_variable(y):
        return unify_var(y, x, theta)
    elif isinstance(x, tuple) and isinstance(y, tuple) and len(x) == len(y):
        for a, b in zip(x, y):
            theta = unify(a, b, theta)
            if theta is None:
                return None
        return theta
    else:
        return None


def standardize_variables(rule):
    """Replaces variables in a rule with fresh unique names and tracks original names."""
    premises, conclusion = rule
    mapping = {}
    reverse_mapping = {}

    def rename(expr):
        if is_variable(expr):
            if expr not in mapping:
                fresh = f"{expr}_{next(var_counter)}"
                mapping[expr] = fresh
                reverse_mapping[fresh] = expr
            return mapping[expr]
        elif isinstance(expr, tuple):
            return tuple(rename(item) for item in expr)
        elif isinstance(expr, list):
            return [rename(item) for item in expr]
        return expr

    return rename(premises), rename(conclusion), reverse_mapping


def is_renaming(s1, s2):
    if s1 != s2 or len(s1) != len(s2):
        return False
    map_1_to_2, map_2_to_1 = {}, {}
    for a, b in zip(s1, s2):
        if is_variable(a) and is_variable(b):
            if a in map_1_to_2 and map_1_to_2[a] != b:
                return False
            if b in map_2_to_1 and map_2_to_1[b] != a:
                return False
            map_1_to_2[a] = b
            map_2_to_1[b] = a
        elif a != b:
            return False
    return True


def match_premises(premises, facts, theta):
    if not premises:
        yield theta
        return
    first, rest = premises[0], premises[1:]
    for fact in facts:
        new_theta = unify(first, fact, theta)
        if new_theta is not None:
            yield from match_premises(rest, facts, new_theta)


def format_atom(atom):
    pred, args = atom
    return f"{pred}({', '.join(args)})"


def format_rule(premises, conclusion):
    lhs = " ∧ ".join(format_atom(p) for p in premises)
    return f"{lhs}  =>  {format_atom(conclusion)}"


def fol_fc_ask_verbose(kb_facts, kb_rules, alpha):
    print("=" * 72)
    print("STEP 1: INITIAL KNOWLEDGE BASE (FACTS & RULES)")
    print("=" * 72)
    print("Initial Atomic Facts:")
    for i, f in enumerate(kb_facts, 1):
        print(f"  F{i}: {format_atom(f)}")

    print("\nDefinite Clauses (Rules):")
    for i, (p, q) in enumerate(kb_rules, 1):
        print(f"  R{i}: {format_rule(p, q)}")

    print(f"\nTarget Query (α): {format_atom(alpha)}")

    print("\n" + "=" * 72)
    print("STEP 2: FORWARD CHAINING EXECUTION TRACE")
    print("=" * 72)

    iteration = 0
    while True:
        iteration += 1
        new_facts = []
        print(f"\n--- Iteration {iteration} ---")

        for r_idx, rule in enumerate(kb_rules, 1):
            orig_p, orig_q = rule
            p_list, q, rev_map = standardize_variables(rule)

            for theta in match_premises(p_list, kb_facts, {}):
                q_prime = substitute(theta, q)

                already_exists = any(
                    is_renaming(q_prime, existing) for existing in (kb_facts + new_facts)
                )

                if not already_exists:
                    clean_theta = {
                        rev_map[k]: v for k, v in theta.items() if k in rev_map
                    }
                    matched_facts = [
                        format_atom(substitute(theta, p)) for p in p_list
                    ]

                    print(f"[Rule R{r_idx} Fired]")
                    print(f"  Rule         : {format_rule(orig_p, orig_q)}")
                    print(f"  Matched Facts: {', '.join(matched_facts)}")
                    print(f"  Substitution : θ = {clean_theta}")
                    print(f"  Inferred Fact: {format_atom(q_prime)}\n")

                    new_facts.append(q_prime)

                    phi = unify(q_prime, alpha, {})
                    if phi is not None:
                        print("=" * 72)
                        print("STEP 3: GOAL REACHED!")
                        print("=" * 72)
                        print(f"Unified {format_atom(q_prime)} with Query {format_atom(alpha)}")
                        print(f"Final Result : TRUE (Substitution φ = {phi})")
                        return phi

        if not new_facts:
            print("No new facts inferred. Stopping.")
            return False

        print(f"End of Iteration {iteration}: Adding {[format_atom(f) for f in new_facts]} to KB.")
        kb_facts.extend(new_facts)


if __name__ == "__main__":
    facts = [
        ("American", ("Robert",)),
        ("Owns", ("A", "T1")),
        ("Missile", ("T1",)),
        ("Enemy", ("A", "America")),
    ]

    rules = [
        ([("Missile", ("x",))], ("Weapon", ("x",))),
        ([("Missile", ("x",)), ("Owns", ("A", "x"))], ("Sells", ("Robert", "x", "A"))),
        ([("Enemy", ("x", "America"))], ("Hostile", ("x",))),
        (
            [
                ("American", ("p",)),
                ("Weapon", ("q",)),
                ("Sells", ("p", "q", "r")),
                ("Hostile", ("r",)),
            ],
            ("Criminal", ("p",)),
        ),
    ]

    query = ("Criminal", ("Robert",))
    fol_fc_ask_verbose(facts, rules, query)
