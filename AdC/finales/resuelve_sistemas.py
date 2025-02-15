from sympy import symbols, Eq, solve

G, O, A, P, s = symbols('G O A P s')
eq1 = Eq(G/1000 + O/1000, A(3/1000))
eq2 = Eq(P10(-5)s + P/1000, -A/1000)
eq3 = Eq(O/1000 + O10(-5)s, P(2/1000) + P10**(-5)s)

sol = solve([eq1, eq2, eq3], [G, O, A])
O_G = sol[O] / sol[G]
print(O_G.simplify())
