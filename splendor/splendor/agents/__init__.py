import glob
import pickle
from datetime import datetime


def filename(agent_name):
    return agent_name + '.agent'

def save(agent_name, agent):
    with open(filename(agent_name) + "." + datetime.now().isoformat(), 'wb') as f:
        pickle.dump(agent, f)

def load(agent_name):
    try:
        pattern = filename(agent_name) + ".*"
        latest = max(glob.glob(pattern))
        with open(latest, 'rb') as f:
            return pickle.load(f)
    except Exception:
        return None
