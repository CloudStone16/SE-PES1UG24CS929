# Reflection

(The handout copy available to me did not list the questions, so these are the four standard Lab 5 reflection questions.)

**1. Which issues were the easiest and which the hardest to fix?**
Easiest: unused imports/variable, trailing whitespace, `!= None`, naming, docstrings, line wrapping; the tool names the line and the fix is mechanical. Hardest: the bare `except: pass` and the missing-ticket `KeyError`s, because deciding the right behaviour (return `False`? raise? log?) is a design choice, and `load_tickets`' `global` rebinding, because it needed thinking about who else holds a reference to the dict.

**2. Did the tools report any false positives, or miss real problems?**
No outright false positives. Bandit B110 (Low) on a tiny try/except/pass looks minor but pointed at a real bug-hiding pattern. R0913 (too many arguments) is arguably noise here since every parameter is a real ticket field; I left it. Missed by all three tools: `closeTicket("99")` crashing with `KeyError`, ids derived from `len()+1` that can collide, and whitespace-only titles. Only running the program and reading the code found those.

**3. How would you integrate static analysis into your workflow?**
Run flake8 + pylint locally via a pre-commit hook for fast feedback, and run all three (including Bandit) in CI on every pull request, failing the build on Bandit Medium/High and on a Pylint score below a threshold. Keep a config file (`.pylintrc`, `setup.cfg`) so any deliberate suppressions are explicit and reviewed.

**4. What tangible improvements did you see?**
Pylint 5.00 -> 9.71, Bandit 2 issues -> 0, Flake8 12 -> 0. Beyond the numbers: no `eval` attack surface, no shared mutable state between calls, files closed reliably, the program no longer crashes on bad input, and every function is documented, so the code is easier to read and review.
