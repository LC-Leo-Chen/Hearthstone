#Effects (can be extended to minions in the future)
#minions
def damage(targets, atk, player):
    for target in targets: target.hp -= atk
def heal(targets, hp_gain, player):#regenerate health, couldn't exceed
    for target in targets: target.hp = min(target.hp + hp_gain, target.max_hp)
def buff_damage(targets, add, player):
    for target in targets: target.attack += add
def buff_health(targets, add, player):#max health and current health are both increased (according to wiki)
    for target in targets: target.max_hp += add; target.hp += add
def polymorph_effect(targets, scalar, player):
    for target in targets:
        if target.card_type == "minion":
            target.attack = 1
            target.max_hp = 1
            target.hp = 1 #since target is not dead its health must originally be non-zero
            target.name = "Sheep"
#card hands
def draw(targets, count, player):
    for _ in range(count): player.draw_card()
def discard(targets, count, player):
    while len(player.hand) > 0 and count: player.hand.pop(); count -= 1 #set.pop() removes an arbitrary element