import itertools
import splendor.agents as agents
from . import trainer
from splendor.agents.idiot import IdiotAgent
from splendor.agents.alpha import AlphaAgent

if __name__ == "__main__":
    agent_name = 'alpha-agent'
    agent = agents.load(agent_name)
    if not agent:
        agent = AlphaAgent(seed=10)
    agents.save(agent_name, agent)

    for (i, _) in enumerate(itertools.repeat(True)):
        print(f"loop: {agent.trainings} / {i}")
        agent = trainer.training_loop(
            agent,
            players=4,
            episodes=1,
            episode_length=1,
            mcts_count=5)

        agents.save(agent_name, agent)
