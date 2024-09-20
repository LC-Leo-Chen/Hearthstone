from Cards import Minion, Spell
import Effects
#Define minions (name, mana cost, attack, health, description, effect list, scalar list, target-type list)
minions=[
      Minion("Chillwind Yeti", 4, 4, 5, "A classic yeti minion with solid stats."),
      Minion("Boulderfist Ogre", 6, 6, 7, "A powerful ogre minion with high attack and health."),
      Minion("Bloodfen Raptor", 2, 3, 2, "A simple raptor minion with good stats for its cost."),
      Minion("Stormwind Champion", 7, 6, 6, "Your other minions have +1/+1.",
            effects=[Effects.buff_health, Effects.buff_damage],
            scalars=[1, 1],
            targetting=["FRIENDLY-O", "FRIENDLY-O"]),
      Minion("Booty Bay Bodyguard", 5, 5, 4, "Taunt", combat_mode="T"),
      Minion("Wolfrider", 3, 3, 1, "Charge", combat_mode="C"),
      Minion("Spymistress", 1, 3, 1, "Stealth", combat_mode="S")
]
#Define minions (name, mana cost, description, effect list, scalar list, target-type list)
spells=[
      Spell("Fireball", 4, "Deal 6 damage.",
            effects=[Effects.damage],
            scalars=[6],
            targetting=["SPECIFIC"]),
      Spell("Polymorph", 4, "Transform a minion into a 1/1 Sheep.",
            effects=[Effects.polymorph_effect],
            scalars=[None],
            targetting=["SPECIFIC"]),
      Spell("Flamestrike", 7, "Deal 5 damage to all enemy minions.",
            effects=[Effects.damage],
            scalars=[5],
            targetting=["ENEMY"]),
      Spell("Arcane Intellect", 3, "Draw 2 cards.",
            effects=[Effects.draw],
            scalars=[2],
            targetting=["NONE"]),
      Spell("Holy Nova", 3, "Deal 2 Damage to all enemy minions. Restore 2 Health to all friendly characters.",
            effects=[Effects.damage, Effects.heal],
            scalars=[2, 2],
            targetting=["ENEMY", "FRIENDLY"]),
      Spell("Cataclysm", 5, "Destroy all minions. Discard 2 cards.",
            effects=[Effects.damage, Effects.damage, Effects.discard],
            scalars=[float("inf"), float("inf"), 2],
            targetting=["ENEMY", "FRIENDLY", "NONE"]),
      Spell("Deadly Shot", 3, "Destroy a random enemy minion.",
            effects=[Effects.damage],
            scalars=[float("inf")],
            targetting=["ENEMY-R"]) #to mark as random selection
]