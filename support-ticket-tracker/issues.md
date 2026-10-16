# Issues found: support_ticket_tracker.py

Line numbers refer to the ORIGINAL file (see `*_report_before.txt`). Ordered by severity.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| `eval()` on a string (B307 / W0123) | Security (Medium) | 91-92 | Code execution sink behind an env var; becomes remote code execution if the string ever carries user input. | Removed the unsafe demo block (and the now-unused `os` import). |
| Bare `except: pass` (B110 / E722 / W0702) | Security (Low) / Bug | 21-26 | Swallows every exception, including `KeyboardInterrupt`; hides real errors. | Catch only `KeyError`, log a warning, return `False`. |
| Mutable default `audit_log=[]` (W0102) | Bug | 10, 16 | One list shared across all calls, so audit entries leak between callers. | Default to `None`; only append when a list is passed. |
| Missing-ticket crashes (not tool-flagged) | Bug | 29-31, 66-67, 70-74 | `update_status`, `closeTicket`, `is_open` raise `KeyError` on unknown id. Typing `99` at the prompt crashed the program. | Use `TICKETS.get()`; return `None`/`False`; `main()` prints "No ticket with id ...". |
| Duplicate ticket ids (not tool-flagged) | Bug | 13 | `len(TICKETS) + 1` reuses an id after tickets are removed/loaded sparse, overwriting a ticket. | `max(existing ids, default=0) + 1`. |
| Blank/whitespace title accepted (not tool-flagged) | Bug | 11 | `"   "` passed the `not title` check. | Check `title.strip()`. |
| `load_tickets` rebinds global (W0603) | Design | 51-54 | `global TICKETS` replaces the dict object; other references go stale. | `TICKETS.clear()` + `update()`; no `global`. |
| `open()` without `with`/encoding (R1732, W1514) | Resource leak | 46-48, 53-55 | File left open if `write`/`loads` raises; platform-dependent encoding. | `with open(..., encoding="utf-8")` and `json.dump/load`. |
| Unused argument `notify` (W0613) | Code smell | 20 | Parameter never used; misleading API. | Removed. |
| Unused variable `count`, imports `sys`, `random` (W0612, W0611, F841, F401) | Dead code | 4, 5, 84 | Dead code. | Removed. |
| `closeTicket` naming (C0103) | Style | 66 | Not snake_case. | Renamed `close_ticket`. |
| `!= None` (C0121, E711, R1714) | Style / Bug-prone | 37 | Identity comparison to `None` should use `is not`. | `status is not None`. |
| Redundant `if/else return True/False` (R1703, R1705) | Style | 71-74 | Verbose boolean return. | Return the boolean expression directly (`in OPEN_STATUSES`). |
| `len()` as truthiness, `%` format, f-string in logging (C1802, C0209, W1203) | Style | 60, 16, 85 | Non-idiomatic. | `not TICKETS`; f-string for audit text; lazy `%d` in `logging.info`. |
| Missing docstrings (C0114, C0116) | Documentation | all | No module/function docs. | Added docstrings. |
| Long lines, trailing whitespace (E501, W291, C0301, C0303) | Style | 10, 14, 63, 71, 79, 80, 84 | Exceed 79 cols; trailing space. | Wrapped lines, removed whitespace. |
| Too many arguments (R0913, R0917) | Design | 10 | `create_ticket` has 6 parameters. | **Not fixed**: all are meaningful ticket fields; refactoring to a dataclass would change the public API. Score is 9.71/10, above the 9.5 target. |

## Results

| Tool | Before | After |
|------|--------|-------|
| Pylint | 5.00/10 (32 messages) | 9.71/10 (2 messages, both the deliberate R0913/R0917) |
| Bandit | 2 issues (1 Medium, 1 Low) | No issues |
| Flake8 | 12 findings | 0 |

Commits: (1) Bandit fixes, (2) Pylint fixes, (3) Flake8 fixes. Reports: `*_report_before.txt` / `*_report_after.txt`.
