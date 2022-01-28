class DotPath:
  def __init__(self, path):
    self._path = path
    self._keys = self._path.split('.')
    self._root = self.keys[0]
    self._branch = '.'.join(self.keys[1:]) if len(self.keys) > 1 else None
  
  @property
  def keys(self):
    return self._keys
  
  @property
  def root(self):
    return self._root
  
  @property
  def branch(self):
    return self._branch
  
  @property
  def is_final(self):
    return self.branch is None
