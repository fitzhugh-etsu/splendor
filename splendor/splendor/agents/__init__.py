import pickle

def filename(agent_name):
    return agent_name + '.agent'

def save(agent_name, agent):
    with open(filename(agent_name), 'wb') as f:
        pickle.dump(agent, f)

def load(agent_name):
    try:
        with open(filename(agent_name), 'rb') as f:
            return pickle.load(f)
    except Exception:
        return None
