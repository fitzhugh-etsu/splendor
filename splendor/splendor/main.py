import itertools

import splendor.agents as agents
from splendor.agents.alpha import AlphaAgent

from . import trainer


def run_training_loop(agent):
    import cProfile
    import pstats
    profiler = cProfile.Profile()
    profiler.enable()
    print("*" * 80)
    print("*" * 80)
    print("*" * 80)
    print("*" * 80)
    print(f"loop: {agent.trainings}")
    print("*" * 80)
    print("*" * 80)
    print("*" * 80)
    print("*" * 80)
    agent = trainer.training_loop(
        agent,
        players=4,
        episodes=1,
        episode_length=16,
        mcts_count=10000)

    agents.save(agent_name, agent)

    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('cumtime')
    stats.dump_stats('agent-training.profile')
    stats.print_stats()


if __name__ == "__main__":
    agent_name = 'alpha-agent'
    agent = agents.load(agent_name)

    if not agent:
        agent = AlphaAgent(seed=10)
    agents.save(agent_name, agent)

    run_training_loop(agent)
