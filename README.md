# AutoHotkey Assignment, Functions & Conditions

Notes: There are some functions which require configuring to your own usage:

- Functions involving the usage of mouse clicks will only work if your display is in 19201080px with zoom scaling set to 100%.
- The OP.GG lookup function requires you to add your player id and tagline to use the default search method.
- The Riot API Key Regenerator requires you To Use Google Chrome to log in to the developer portal.
- The Next Page Function requires you to specify the location of the next page button on the screen after pressing the "End" Key (The "Window: X, Y" Coordinates in the Window Spy Tool).

---

## Using The OPGG Scraper

### Prerequisties

- Python version 3.9.13 or later.
- Must install dependencies using <code>pip install -r requirements.txt</code>.

---

### Pulling & Cleaning OPGG Data

1. Navigate to the scripts directory.
2. Run the opgg_scraper.py script with the following arguments:

   - Summoner Name (If name includes spaces put quotes around it. Example: 'Hide on Bush')
   - Tag (No #)
   - Season Number
     - 27 = 2024 S2
     - 25 = 2024 S1
     - 23 = 2023 S2
     - 21 = 2023 S1
     - 19 = 2022
     - 17 = 2021
     - 15 = 2020
     - 13 = Season 9
     - 11 = Season 8
     - 7 = Season 7
     - 6 = Season 6
     - ...etc

   Example: <code>python opgg_scraper.py Fire 2842 27</code>.

3. Repeat Step 2 for all desired seasons.
4. Run the parse_stats.py script with the following arguments:

   - Summoner Name
   - Season Number

   Example: <code>python parse_stats.py Fire 27</code>.

5. Repeat step 4 for all desired seasons.
6. A directory named Data will be created with a unique directory for each summoner that is searched for.
   - Inside each summoner Directory there will be individual Season stat Jsons where the specific stats for that season may be viewed.
   - There will also be a single Season Stats json which will include data from all seasons that have been processed.

---

## HotKeys

<pre>
Hotkey Format:
### OR #### "Modifer"
- Assigned Key , Function
  - Conditional Requirements
</pre>

### No Modifier

- Numpad0 , Discord Mass Share, DISABLED
  - Discord Active

### Single Modifier

#### "Ctrl + "

- O , Open OP.gg and close Adblock

  - Always Active

- R , Reload Primary, DISABLED

  - Not Active League In Game

- E , Edit Primary, DISABLED
  - Not Active League In Game AND Not Active VSCode

#### "Shift + "

#### "Alt + "

- Mouse Button4 , Audio Sampler, DISABLED

  - Chrome Active OR Spotify Active, AND Not Active League In Game

- M , Go To Match History

  - League Client Active

- C , Go To Challenges

  - League Client Active

- L , Open Lolalytics Matchup data based on Champion, Patch, & Lane
  - Always Active

#### "Win + "

### Multi-Modifier

#### "Ctrl + Alt + "

- P , Pause Scripts, DISABLED
  - Always Active

#### "Ctrl + Shift + "

---

## Hot Strings

<pre>
Hotstring Format:
### OR #### Hotstring Type
- Trigger String , Function
  - Conditional Requirements
</pre>

### Text Inserts

- Datacomp , Lolalytics Data Template
  - Always Active

### Hot Functions

- Keyregen , Riot APi Key Regenerator
  - Chrome Active

#### "play- + "

- Normal , Start Normal League Game
  - Always Active
- Ranked , Start Ranked League Game
  - Always Active
- TFT , Start TFT Game
  - Always Active
- Aram , Start Aram Game
  - Always Active
- Arena , Start Arena Game
  - Always Active
