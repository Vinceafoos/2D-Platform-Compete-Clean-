# Compete Clean – Game Design Document

## Vincent Ryan & Liam Davis

![ss](screenshots/top_gdd_ss.png)
## Introduction

### Game Summary
Compete Clean is a 2D platformer where players take on the role of a World Anti-Doping Agency (WADA) agent tasked with collecting evidence across three increasingly difficult levels. Players must navigate obstacles, beat a time limit, and collect blood samples to build a case against a suspected athlete. The outcome depends on how much evidence is gathered, leading to either justice or failure.

### Inspiration
Doping in athletics has always been a problem. And while organizations like WADA exist in order to prevent cheating, the challenge of catching and successfully exposing such people is often much more complicated. We hope to bring light to the doping situation in sports while allowing the player to engage in an interesting and challenging mission as a WADA agent. 

For our art style we took some general inspiration from Kirby's Adventure which has a light, visually pleasing retro feel as it is a classic 8-bit game. We also drew from the Super Mario Bros 2 mechanic of the charge jump into our game, which allows the player to charge their jump for a limited amount of time in order to reach higher locations. 

---

## Concept

### Gameplay Overview
The player controls a WADA agent navigating through three levels, attempting to collect enough evidence within a specified time limit.

### Theme Interpretation

#### Action Codes
The narrative unfolds through different gameplay actions, which serve as the primary storytelling device:
- Navigating hazards (javelin throwers, spike traps, sand pits)
- Performing precise and high jumps
- Racing against a time limit to gather evidence
All of these actions help drive the story of the game on. 

Each obstacle represents resistance, not all realistic to the world, but still symbolic of the difficulty when uncovering truth in a system that is known to resist exposure. As the player progresses through levels, the intensity increases, creating narrative escalation.

#### Enigma Codes
The game begins with a question regarding the integrity of an athlete, the player is not explicitly told the person you're after is cheating, instead it is something you must uncover. This uncertainty frames some of the experience. There is a bit of mystery, and to solve it the player must collect evidence scattered across increasingly difficult levels. Each collected item gets you closer to answering the mystery, but never fully resolves it until the end. 

#### Look and Feel
Visually, Compete Clean uses a retro, pixel art style, forming a light and approachable tone, which we then contrast with the serious underlying theme of doping and corruption. The player should be visually pleased as they navigate levels and collect evidence, but have a sense of importance as their performance has an impact in serving justice.

---

## Mechanics

### Primary Mechanics
| Mechanic| Description | Image |
|---|---|---|
| Movement | The player can traverse the level by moving left and right. | ![walking](md_assets/walking.png) |
| Jump | By pressing space the player can jump over obstacles, or onto higher surfaces. | ![jumping](md_assets/jump.png) |
| Charge Jump | By holding down the down key, the player can charge their jump to reach higher locations.  | ![charging](md_assets/charge_jump.png) |
| Wind | There is a 1/5 chance of a windy day each level, which effects player movement. | ![wind](md_assets/wind.png) |

### Secondary Mechanics
| Mechanic| Description | Image |
|---|---|---|
| Javelin Thrower |  The player will have to avoid javelins being thrown in their direction as they complete the mission. | ![jav thrower](md_assets/jav_thrower.png) |
| Spike | Some doped up track spikes have gotten loose, and the player must avoid them to not take damage. | ![spike](md_assets/spike.png) |
| Sand Trap |  Slows player movement | ![sand pit](md_assets/sand_pit.png) |
| Weights |  The player can pick up weight items which will increase their max High Jump ability. | ![weight item](md_assets/weight.png) |
