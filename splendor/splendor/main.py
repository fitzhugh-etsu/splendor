import itertools
import splendor.agents as agents
from . import trainer
from splendor.agents.idiot import IdiotAgent

if __name__ == "__main__":
    agent_name = 'idiot-agent'
    agent = agents.load(agent_name)
    if not agent:
        agent = IdiotAgent(seed=10)
    agents.save(agent_name, agent)

    for (i, _) in enumerate(itertools.repeat(True)):
        print(f"loop: {agent.trainings} / {i}")
        agent = trainer.training_loop(
            agent,
            players=4,
            episodes=2,
            episode_length=10,
            mcts_count=10)

        agents.save(agent_name, agent)





