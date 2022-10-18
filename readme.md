# Osu Bracket Filler
Pretty simple script to automate filling up the bracket file, since default interface provided by osu!lazer tournament client is too cumbersome when you have to fill up EVERY single match on the ladder, especially when your tournament starts at RO64.

## Features
- Filling up teams with players
- Filling up players as teams
- Filling up mappools
- Importing challonge ladder
- Simple command line interface.

## Usage
1. Paste the stuff you're asked about ([bancho key](https://osu.ppy.sh/p/api/), [challonge key](https://challonge.com/settings/developer)).
2. Select what parts of script would you like to run.
3. Open bracket file you'd like to edit.
4. Select file with data (or just cancel to open default one in your textfile editor)
5. Done! In case something broke just rename lastest backup file to bracket.json.

**You can get empty bracket templates [here](https://drive.google.com/drive/folders/1xkMeKuUYl9wp4I-VJzM2P8XOUlWGiX1f)**. _(thanks, jh1h1h)_

## Supported data formatting

### Mods
This file is used for adding additional mods (NM, HR, HD) of your choice.

### Mappool
For now only this formatting is avaiable:

`(Name of the round, i.e. Quarterfinals)`

`(modname)(tab key)(map id)`

**Example**

```csv
Round Of 32
NM1	1737389
NM2	3335664
NM3	3601683
NM4	3756543
NM5	3448872
HD1	1513623
HD2	2283643
HR1	3274114
HR2	1592403
DT1	859034
DT2	2145491
DT3	2015326
FM1	2278201
FM2	96095
TB1	821273
```

### Teams
The following formatting is available:
1. `(Username)`
2. `(Teamname)(tab key)(Username 1/User Id 1)(tab key)(Username 2/User Id 2) ...`
3. This one too!
```csv
(Teamname) (seed 1)
(Teamname) (seed 2)
...
(Teamname) (seed 1)(tab key)(Username 1/User Id 1)(tab key)(Username 2/User Id 2) ...
```
First you get teamnames in (in seeding's order), then just add usernames or user ids.
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

## Running the source code.

1. Download the source code (preferably through git tools).
2. Run the `pip install -r requirements.txt` to download dependencies.
3. Hope nothing breaks (and report bugs, please)!