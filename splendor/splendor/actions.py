from .models.actions import ValidPlayerActions, ValidGemPaybackActions, PerformedAction

def eval_action(game, action_enum):
    return action_enum.value[0](game, *action_enum.value[1])

def valid_actions(game, yield_invalid=False):
    for action in ValidPlayerActions:
        new_game = eval_action(game, action)
        if new_game:
            yield PerformedAction(action=action, game=new_game)
        elif yield_invalid:
            yield None

def valid_payback_actions_for_last_player(game, yield_invalid=False):
    for action in ValidGemPaybackActions:
        new_game = eval_action(game, action)
        if new_game:
            yield PerformedAction(action=action, game=new_game)
        elif yield_invalid:
            yield None

def valid_nobles_for_last_player(game, yield_invalid=False):
    for action in ValidNobleActions:
        new_game = eval_action(game, action)
        if new_game:
            yield PerformedAction(action=action, game=new_game)
        elif yield_invalid:
            yield None

def all_actions():
    for action in ValidNobleActions:
        new_game = eval_action(game, action)
        if new_game:
            yield PerformedAction(action=action, game=new_game)


def next_game_actions(game):
    # If there are > 10 we need to give some gems back
    if (actions := list(valid_payback_actions_for_last_player(game))):
        return (False, actions)
    # If there are nobles, we need to accept some
    if (actions := list(valid_nobles_for_last_player(game))):
        return (False, actions)

    # Otherwise
    return (True, list(valid_actions(game)))

def gem_return_action(game, affinity, seed=None):
    more = True

    while more:
        action_list = list(valid_payback_actions_for_last_player(game, yield_invalid=True))
        more = any(action_list)

        if more:
            action = random.Random(seed).choices(
                action_list,
                weights=[(action_list[i] and affinity[i]) or 0
                         for i in
                         range(len(action_list))])
            return action[0]
    return None

def noble_accept_action(game, affinity, seed=None):
    more = True

    while more:
        action_list = list(valid_nobles_for_last_player(game, yield_invalid=True))
        more = any(action_list)

        if more:
            action = random.Random(seed).choices(
                action_list,
                weights=[(action_list[i] and affinity[i]) or 0
                         for i in
                         range(len(action_list))])
            return action[0]
    return None

def evaluate_player_intent(game, agent_intent, seed=None):
    player_i = game.turn % len(game.players)

    possible_outputs = io.outputs(game)

    # Pick action
    action_p = [(possible_outputs[i] and agent_intent.action_probabilities[i]) or 0
                for i in
                range(len(agent_intent.action_probabilities))]

    if any(action_p):
        action = random.Random(seed).choices(
            possible_outputs,
            weights=action_p,
            k=1)[0]

        #  TODO??????
        #  WHY NULL?
        if not action:
            import pudb; pudb.set_trace()

        print(f"Player {player_i} chose {action.action}")
        # Now check for payback gems
        while (gem_action := gem_return_action(game, agent_intent.resource_affinity, seed=seed)):
            print(f"Player {player_i} decided {gem_action.action}")
            action = gem_action
            game = action.game

        # Now check for noble visits
        if (noble_action := noble_accept_action(game, agent_intent.noble_affinity, seed=seed)):
            print(f"Player {player_i} decided {noble_action.action}")
            action = noble_action
            game = action.game
    else:
        print(f"Player {player_i} PASSES")
        action =  PerformedAction(
            action=None,
            game=pass_turn(game))

    return action
