# Parity allowlist

Each line is a substring; a CSS or DOM diff line containing it is an accepted, documented
deviation from the B787 original. Anything else parity_diff.py reports is a defect.

- --goodtext
- ${d.cond?
- data:image/svg+xml
- assets/icons/
- assets/A330_hero.svg
- <tbody>

The last five cover the placeholder logo SVG (an inline data URI) and the sixth footer row (AFM), which the B787 table does not have.
- +svg 
- +text 
- +tr 
- +td 
- +a 
