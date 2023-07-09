import random

class ProxyLoader:

    def __init__(self, li, order='seqential'):
        self.list = li
        self.order = order
        self.cur = 0
        
    def __iter__(self): return self
        
    def __next__(self):
        if self.list is None or len(self.list) == 0:
            return None
        elif self.order == 'seqential':
            p = self.list[self.cur]
            self.cur += 1
            return {'http': p, 'https': p}
        elif:
            p = random.choice(self.list)
            return {'http': p, 'https': p}
            