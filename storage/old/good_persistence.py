import json

class Storage:
  def __init__(self, base=None, key=None, value={}):
    object.__setattr__(self, '_cache', value)
    object.__setattr__(self, '_base', base)
    object.__setattr__(self, '_key', key)
    object.__setattr__(self, '_responders', {})
  
  def __getattr__(self, key):
    value = self._cache[key]
    if isinstance(value, dict):
      value = Storage(self, key, value)
    return value

  def __setattr__(self, key, value):
    self._cache[key] = value
    self._base._update(key, self._cache)

  def __repr__(self):
    return str(self._cache)

  def register(self, responder, path):
    self._responders[path] = responder


class FSStorage(Storage):
  def __init__(self, filepath):
    object.__setattr__(self, '_filepath', filepath)
    try:
      with open(self._filepath, 'r') as f:
        j = json.load(f)
    except:
      j = {}
    super().__init__(self, None, j)
    self._update(None, None)

  def _update(self, key, value):
    with open(self._filepath, 'w') as f:
      json.dump(self._cache, f)






print('hello world')

def responder(path, value):
  print(f'this is the responder for path: {path} and value {value}')

s = FSStorage('test.txt')
s.register(responder, 'activate.method')



