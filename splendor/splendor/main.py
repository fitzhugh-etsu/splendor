import splendor.agents as agents
from splendor.agents.alpha import AlphaAgent
from splendor.agents.idiot import IdiotAgent

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
        episodes=10,
        episode_length=16,
        mcts_count=5000)

    agents.save(agent_name, agent)

    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('cumtime')
    stats.dump_stats('agent-training.profile')
    stats.print_stats()


if __name__ == "__main__":
    import sys

    agent_name = 'agents/' + sys.argv[1]  # 'alpha-agent'
    agent = agents.load(agent_name)

    if not agent:
        agent = AlphaAgent()
        agents.save(agent_name, agent)

    #agent = IdiotAgent()
    run_training_loop(agent)
