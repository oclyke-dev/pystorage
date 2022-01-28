import json

from storage import RootStorage
import tests

class FSStorage(RootStorage):
  def __init__(self, filepath, default={}):
    object.__setattr__(self, '_filepath', filepath)
    try:
      with open(self._filepath, 'r') as f:
        initial = json.load(f)
    except:
      initial = default
    super().__init__(initial)
  
  def _final(self, value):
    with open(self._filepath, 'w') as f:
      json.dump(self._cache, f)


tests.test_set()
tests.test_get()
tests.test_get_invalid()
tests.test_access()
tests.test_responders()

print('all tests passed')

