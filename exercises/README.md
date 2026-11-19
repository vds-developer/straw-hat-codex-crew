# Crew trials

Give Luffy one brief below. For each numbered check, record the command or interaction, the expected result, and the observed result. Count how many checks pass on the first handoff to the verifier. If a handoff misses a case, revise the brief or crew instructions in one place, then rerun the same check and record what changed.

## Running the tools

Run these commands from the repository root.

- `pwsh -NoProfile -File tools/Test-CrewProfiles.ps1` checks the crew profiles. It uses Python 3.11+ or Python with `tomli` installed. Append `-ProfilesPath DIRECTORY` to check a different profile directory.
- `python exercises/score_trial.py exercises/example-score.json` scores an illustrative trial. To score your run, copy the example, record each check and its evidence, then pass your copy to the command. The exit code is 0 when every check passes, 1 when a check fails, and 2 for invalid input.

## 1. Reconcile a shipment

Build a local command that reads a CSV with the columns `item,quantity`. Sum signed integer quantities by item, then emit an `item,total` CSV sorted by item. Nami specifies the command arguments, Franky implements the command, and Usopp checks the output using a new input file.

1. Supply the rows `rope,3`, `bolt,5`, and `rope,-1`. Expect the header followed by `bolt,5` and `rope,2`, in that order.
2. Supply the row `"bolt, brass",4`. Reading the output with a CSV reader must yield the two values `bolt, brass` and `4`.
3. In the file from check 1, change `bolt,5` on line 3 to `bolt,many`. Expect a nonzero exit, a diagnostic identifying line 3 on stderr, and empty stdout.

## 2. Pack a day bag

Build a single local web page with three checkboxes labeled Water, Map, and Coat, a packed-item count, and a Reset button. Persist selections across reloads. Brook owns the page. Usopp exercises the keyboard flow, and Zoro reviews the reset behavior.

1. Open the page in a fresh browser profile. Expect three unchecked boxes and a count of 0 of 3.
2. Reach Map with Tab and toggle it with Space. Expect a count of 1 of 3. Reload and confirm Map alone is checked and the count is still 1 of 3.
3. Activate Reset using the keyboard, then reload. Expect all boxes unchecked and a count of 0 of 3.

## 3. Repair a room calendar

The calendar compares two bookings on the same day, specified in 24-hour local time. Start with a disposable command that reports a conflict whenever the later start is **less than or equal to** the earlier end. Adjacent bookings should be allowed. Chopper demonstrates the failure, Franky repairs the comparison, and Usopp repeats the checks through the command.

1. Compare 09:00–10:00 with 10:00–11:00. Record the original `conflict` and the required result `available`.
2. Compare 09:00–10:00 with 09:59–11:00. Expect `conflict` in either argument order.
3. Compare 09:00–12:00 with 10:00–11:00. Expect `conflict`. Move the second booking to 13:00–14:00 and expect `available`.
