# Osu Bracket Filler
Pretty simple script to automate filling up the bracket file

## Features
- Filling up teams w/ players
- Filling up mappools
- Importing challonge ladder
- Simple command line interface

## Usage
1. Paste the stuff you're asked about ([bancho key](https://osu.ppy.sh/p/api/), [challonge key](https://challonge.com/settings/developer), challonge username).
2. Select functions to run.
3. Open bracket file you'd like to edit.
4. Select file with data (or just cancel to open default one in your textfile editor)
5. Done! In case something broke just rename lastest backup file to bracket.

## Supported data formatting

### Mods
This file is used for adding additional mods (NM, HR, HD) of your choice.

### Mappool
For now only this formatting is avaiable:

`(Name of the round, i.e. quarterfinals)`

`(modname)(tab key)(map id)`

### Teams
The following formatting is available:
1. `Username`
2. `Teamname(tab key)Username 1/User Id 1(tab key)Username 2/User Id 2 ...`
3. This one too!
```csv
Teamname (seed 1)
Teamname (seed 2)
...
Teamname (seed 1)(tab key)Username 1/User Id 1(tab key)Username 2/User Id 2 ...
```
#### Examples
1.
```csv
Kevorc
RemIscute07
Tsukime
EulaFootEnjoyer
_Kasaezic
I dunno
Filtrator
CPU_Cartel
```
2.
```csv
HD2 ban	Neotopisch	_Ene	EulaFootEnjoyer	tplc	Jabbruh
I dunno 	_Kasaezic	MyAimGenoKiller	Akagii	GreenKusa	tomatohung
100% Illegal Team	flyond	RemIscute07	Nuit_	Tsukime	comm899
TBD	Cittasnaf	CPU_Cartel	Filtrator	Kevorc
```
3.
```csv
First Team!
HD2 ban	Neotopisch
I dunno
100% Illegal Team
TBD
Random Team!
HD2 ban	Neotopisch	_Ene	EulaFootEnjoyer	tplc	Jabbruh
I dunno 	_Kasaezic	MyAimGenoKiller	Akagii	GreenKusa	tomatohung
100% Illegal Team	flyond	RemIscute07	Nuit_	Tsukime	comm899
TBD	Cittasnaf	CPU_Cartel	Filtrator	Kevorc
```