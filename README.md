# ev_to_bids

Creates BIDS formated TSV file from input FSL stimulus files.

```
usage: ev_to_bids.py [-h] -n STR -s FILE -o TSV

Constructs BIDS formatted TSV file from input FSL-style custom 3-column format
stimulus files. NOTE: the options '-s' and '-n' are repeatable.

optional arguments:
  -h, --help            show this help message and exit

Required arguments:
  -n STR, --name STR    Name (label) of stimulus [Repeatable].
  -s FILE, --stimulus FILE
                        Input stimulus file [Repeatable].
  -o TSV, --out TSV     Output TSV (tab separated values) file to be written.
```
