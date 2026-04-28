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


**Next/TO DO :**  
* Add transition screens
* Start working on enemies 
