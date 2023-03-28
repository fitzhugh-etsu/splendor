import itertools

import splendor.agents as agents
from splendor.agents.alpha import AlphaAgent
from splendor.agents.idiot import IdiotAgent

from . import trainer

if __name__ == "__main__":
    agent_name = 'alpha-agent'
    agent = agents.load(agent_name)
    print(agent.__class__)
    if not agent:
        agent = AlphaAgent(seed=10)
    agents.save(agent_name, agent)

    for (i, _) in enumerate(itertools.repeat(True)):
        print(f"loop: {agent.trainings} / {i}")
        agent = trainer.training_loop(
            agent,
            players=4,
            episodes=10,
            episode_length=10,
            mcts_count=1000)

        agents.save(agent_name, agent)
