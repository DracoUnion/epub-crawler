import random
from .config import config
from threading import Lock

class ProxyLoader:

    def __init__(self, li=None, order='seqential'):
        self.list = li
        self.order = order
        self.cur = 0
        self.lock = Lock()
        
    def __iter__(self): return self
        
    def __next__(self):
        if self.list is None or len(self.list) == 0:
            return None
        elif self.order == 'seqential':
            with self.lock:
                p = self.list[self.cur]
                self.cur += 1
                return {'http': p, 'https': p}
        elif:
            p = random.choice(self.list)
            return {'http': p, 'https': p}
            
config['proxyLoader'] = ProxyLoader()
            