# What never gets published

This file is the sanitizer exception. It names the patterns the CI script blocks in every other file. Keep real private data out of this file too. The secret scan still reads it.

## Blocked by the script

The script `scripts/check_sanitized.py` fails the build when any other file contains:

- An email address. Example shape, fake: person@example.com
- A phone number. Example shape, fake: (000) 000-0000
- A run of 6 or more digits. Example shape, fake: 000000
- The whole word password
- The whole word token

The script skips this path so the checklist can name those patterns. Do not copy the examples into another file.

## Also keep out, even though you have to notice them yourself

- Account numbers, including a masked number. Describe the rule ("masked to the last 4"). Do not print digits from an account.
- Balances
- Transactions
- Mortgage information
- Credit information
- Trading results, profit, loss, tickers, and trade history
- Real chat contents and real email or message text
- Credentials, keys, and session material
- Internal system ids and internal URLs
- Names of real third parties
- A real morning brief, a real calendar, or a real usage export
- Screenshots of a live inbox, brokerage, calendar, or dashboard

The HQ image in this repo is an illustrative mock. Replace it only with a shot that has been through this list.

## Before you fill an Outcomes line

1. Write the result from your own records.
2. Remove other people's names, message text, and figures you do not want public.
3. Run `python scripts/check_sanitized.py`.
4. If it fails, the printed line is the line to rewrite.

## Related

- [README](../README.md)
- [Operating rhythm](operating-rhythm.md)
