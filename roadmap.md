### Date: 4/15
**Goal**
Make initial files and classes

**Implementation**
*Technical Plan/Credit*: Used starter code from (https://github.com/NguyenLe15325/Python-raylib/blob/main/11.2D_platformer_clone.py)
*Content Credit*:

**Commit message**
Creating player and enemy files

**Next/TO DO :**
* Make GDD
* Create items
* Handle collisions between players and items

---

### Date: 4/16  
**Goal**  
Finish GDD v1

**Implementation**  
*Technical Plan/Credit*: Drafted and finalized the GDD, outlining core mechanics, items, overall game structure, and the story
*Content Credit*: Images in the GDD were generated using ChatGPT

**Commit message**  
gdd v1 final  

**Next/TO DO :**  
* Add basic player movement physics  
* Add items
* Begin implementing collision system

---

### Date: 4/20  
**Goal**  
Implement collision system 

**Implementation**  
*Technical Plan/Credit*: Built initial collision detection between player and environment tiles using bounding boxes and tile-based checks  
*Content Credit*: N/A  

**Commit message**  
v1, collisions still not right  

**Next/TO DO :**  
* Fix collision inconsistencies   
* Add items
* Implement collision system

---

### Date: 4/22  
**Goal**  
Expand gameplay systems (enemies, items, movement)  

**Implementation**  
*Technical Plan/Credit*:  
- Improved collision between player and the level  
- Implemented items (blood and weight)  
- Added charge jump mechanic 
- Created enemy subclasses which thrower extends

*Content Credit*:  
- Player sprite sheet added, created by ChatGPT and then edited/resized by us

**Commit message**  
(feat) blood and weight and charge jump  
feat(thrower): added thrower class extending enemy  
fix(collision): player collisions with obstacles  
Main player sprite sheet added  
new sprite sheet sizing  

**Next/TO DO :**  
* Use our character sprite  
* Start animating the character  

---

### Date: 4/26  
**Goal**  
Insert and animate our character  

**Implementation**  
*Technical Plan/Credit*: Integrated custom player sprite into the game and began animating it
*Content Credit*: 

**Commit message**  
(feat) added our own sprite to game  

**Next/TO DO :**  
* Refine character animations
* Start tracking item collection with some kind of UI
* Add textures for items

---

### Date: 4/27  
**Goal**  
Add HUD and item visuals  

**Implementation**  
*Technical Plan/Credit*:  
- Implemented HUD displaying evidence, strength, and time  
- Added blood bag texture 

*Content Credit*: Blood bag texture from ChatGPT  

**Commit message**  
(feat) HUD with counter for evidence, strength, and time  
(feat) blood bag texture added  

---

### Date: 4/28  
**Goal**  
Make jumping more smooth and fix various problems with it

**Implementation**  
*Technical Plan/Credit*:  
- Fix the animation of charging the jump
- Don't allow the player to charge while moving

*Content Credit*: 

**Commit message**  
fix(charge): no longer can move while charging
feat(weight): texture on weight and crouch bug fix
(fix) can no longer jump mid air if falling off a platform
fix(charge): fix charge animation

**Next/TO DO :**  
* Start adding transitions between levels
* Start working on enemies 

---

### Date: 4/29
**Goal**  
Add Textures into the world

**Implementation**  
*Technical Plan/Credit*:  
- Using Photoshop

*Content Credit*: Gemini 3 Pro for base images and Adobe Photoshop for editing

**Commit message**  
feat(world textures): added temporary world textures

**Next/TO DO :**  
* Work on enemy sprite sheet and implementation

---

### Date: 4/30
**Goal**  
Make javelin sprite sheet and other features
**Implementation**  
*Technical Plan/Credit*:  
- Add javelin sprites to wada sheet with photoshop
- Implement sand that slows you down and lowers your jump
- Improve debug mode to skip through levels

*Content Credit*: 

**Commit message**  
(feat) can now skip thru levels in debug mode, levels now loaded in from a csv
fix(javelin character sprite sheet)
(feat) added sand that slows you down and shortens your jump
feat(javelin player texture pack)

**Next/TO DO :**  
* Work on win conditions

---

### Date: 5/1
**Goal**  
Create a placeholder screen for winning
**Implementation**  
*Technical Plan/Credit*:  
- Add a new game state for the end of the game, draw stats from the game on it at the end
- Also change the weight mechanic so you need at least one weight to do a charge jump

*Content Credit*: 

**Commit message**  
(feat) there is now a win screen with stats
(feat) update levels & now need at least 1 weight to do a charge jump

**Next/TO DO :**  
* Implement our javelin enemy
* Create the actual splash/win/lose screens

---

### Date: 5/2  
**Goal**  
Add presentation screens, level completion feedback, and improve gameplay polish  

**Implementation**  
*Technical Plan/Credit*:  
- Added a splash screen for the game  
- Added level completion screens with player stats  
- Implemented functional javelin thrower behavior  
- Adjusted charge jump heights  
- Fixed the charge indicator so stars scale based on charge percentage  

*Content Credit*:  
- All screens for the game were generated using ChatGPT

**Commit message**  
(feat) splash screen added  
feat(javelin thrower): functional javelin thrower & bug fixes  
fix(world): bottom layer fix  
fix(charge): adjust charge heights  
(feat) now displays level completion screens with stats  
feat(charge indicator): stars scale with % of charge done  
refactor(thrower & javelin): add unload and restructure files  
feat(In-game background): temporary in game background  

**Next/TO DO :**  
* Continue polishing game screens and transitions  
* Add win/lose conditions  
* Improve enemy behavior and level hazards  

---

### Date: 5/3  
**Goal**  
Finish core game flow, add more hazards, audio, pause/instruction screens, and improve performance  

**Implementation**  
*Technical Plan/Credit*:  
- Added win, lose, calculating result, instructions, and replay screens  
- Added level completion and game ending logic  
- Added finish line to complete levels  
- Added player death when health runs out, with options to restart the level or restart the game  
- Added pause functionality using P  
- Added game music  
- Added pickup sounds for blood and weight items  
- Added spike hazards and damage feedback  
- Randomized javelin throws  
- Made blood bag spawns less predictable  
- Added floating clouds and cloud files: Help from Claude
- Added item gain notifications and level name popups  
- Updated HUD design and adjusted HUD sizing  
- Improved performance by unloading assets, garbage collecting javelins, and removing unnecessary rectangles from drawing
- Added Wind
- Added Wind movement: Help from Claude

*Content Credit*:  
- These screens were also generated from ChatGPT.
- Audio will be cited in our GDD 

**Commit message**  
(feat) win/lose/calculating result screens added, can replay after finishing  
(feat) blood bags now don't always spawn  
(fix) slight level changes  
fix(jav throw): randomized throws  
(feat) player now dies if runs out of health, can restart level or game  
feat(spikes): added spike png  
feat(spikes and damage notice): flicker to know when took damage  
fix(sheets): changes in spritesheets  
(feat) added a finish line  
fix(map and javs): garbage collect javs & map updates  
(feat) Can now pause using P  
(fix) Pause now follows camera  
(feat) Instructions screen added  
feat(clouds): cloud files  
(feat) game music added  
(feat) pickup sounds for the blood and weight  
(fix) improved some performance and unloaded everything  
(fix) fixed bug where if you get to the end twice in one sitting the calculating screen doesnt work  
feat(clouds): floating clouds  
(fix) more performance fixes (taking rectangles out of drawing)  
fix(hud): new hud  
fix(hud): small size change  
feat(popups and level name): notifcation when gaining items 
feat(wind): wind chance and bug fixes


---
