best_network = RandomNetwork()

def MonteCarloTreeSearch():
  # Uses tree search and propagates either the NN
  #  evaluation of the node or a -1/1 for loss/victory

def Train():
  # Attempts to train a network with it's history of moves
  #  if won re-inforce, if lost, de-inforce

def PitNetworks():
  # Return a set of networks, replacing a player with the
  #  best_network so far.

for episode_number in range(NUMBER_OF_SERIES_TO_TRAIN):
  episode_networks = best_network[NumberOfPlayers]
  for game_number in range(NUMBER_OF_GAMES_PER_SERIES):
    game_state = NewGame()

    while NotFinished(game_state):
      for player in Players():
        p_next_move = MonteCarloTreeSearch(
                        game_state,
                        iterations=1600,
                        neural_net=episode_network[player],
                        temperature=TempFunction(episode_number))

        next_move = SelectNextMove(p_winning, p_next_move)

        game_state = MakeMove(game_state, next_move)

    winner = Winner(game_state)
    # Train networks
    for player in Players():
      episode_networks[player] = Train(
                                  episode_networks[player],
                                  GetPlayerMoves(game_state, player),
                                  weight=(player == winner ? 1 : -1))

    # Compete!
    wins = int[Players() + 1]
    for player in Players():

      for pit_game in range(PIT_GAMES):
        # Replace one network with the current best network (once for each player)

        networks = PitNetworks(
                    episode_networks
                    best_network,
                    player)
        winner = PlayGame(networks)
        if player == winner:
          # Best Network Won
          wins[4] += 1
        else:
          wins[player] += 1

    # If one performed measurably better than the previous best
    best = max(mean(wins))
    if (best - mean(wins)) > (PIT_GAMES * Players() * WIN_PCT_THRESHOLD):
      best_network = best
