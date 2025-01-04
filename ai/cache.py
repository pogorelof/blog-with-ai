class Cache:
    def __init__(self):
        self.cache = {}
    
    def check(self, key):
        return key in self.cache
    
    def get(self, key):
        return self.cache[key]
    
    def set(self, key, content):
        self.cache[key] = content