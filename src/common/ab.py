import hashlib, random, yaml
from typing import Optional, Dict, Any

class ABRouter:
    def __init__(self, config_path: str):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.cfg = yaml.safe_load(f)

    def route(self, headers: Dict[str,str], user_id: Optional[str]) -> Dict[str,Any]:
        # Header match first
        for exp in self.cfg.get('experiments', []):
            m = exp.get('match')
            if m and headers.get(m.get('header')) == m.get('value'):
                return {'experiment': exp['name'], 'mode': exp.get('traffic','control'), 'overrides': exp.get('treatment',{})}
        # Hash-based split
        for exp in self.cfg.get('experiments', []):
            percent = exp.get('percent')
            if percent and user_id:
                h = int(hashlib.sha1((user_id + exp.get('name','')).encode()).hexdigest(), 16) % 100
                if h < percent:
                    return {'experiment': exp['name'], 'mode': 'treatment', 'overrides': exp.get('treatment',{})}
        return {'experiment': 'control', 'mode': 'control', 'overrides': {}}
