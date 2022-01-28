
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
  

class Storage:
  def __init__(self, base, key):
    object.__setattr__(self, '_cache', {})
    object.__setattr__(self, '_base', base)
    object.__setattr__(self, '_key', key)
    object.__setattr__(self, '_responders', {})
  
  def __setattr__(self, key, value):
    self._cache[key] = value
    self._bubble(key, value)
  
  def __getattr__(self, key):
    return self._cache[key]

  def __repr__(self):
    return str(self._expand())
  
  def _expand(self):
    e = {}
    for key, value in self._cache.items():
      try:
        e[key] = value._expand()
      except AttributeError:
        e[key] = value
    return e
  
  def _bubble(self, key, value):
    self._try_responders(key, value)
    self._base._bubble(self._key, self._cache)
  
  def _try_responders(self, key, value):
    try:
      for responder in self._responders[key]:
        responder(value)
    except KeyError:
      pass

  def _cache_at(self, path):
    p = DotPath(path)
    if p.is_final:
      return self._cache[p.root]
    else:
      return self._cache_at(p.branch)

  def _register(self, responder, path):
    p = DotPath(path)
    if p.is_final:
      try:
        self._responders[p.root].append(responder)
      except KeyError:
        self._responders[p.root] = [responder]
    else:
      self._cache[p.root]._register(responder, p.branch)
      
  def _deregister(self, responder, path):
    p = DotPath(path)
    if p.is_final:
      try:
        self._responders[p.root] = list(filter(lambda r: r is not responder, self._responders[p.root]))
        if len(self._responders[p.root]) == 0:
          del self._responders[p.root]
      except KeyError:
        pass
    else:
      self._cache[p.root]._deregister(responder, p.branch)
    pass

    
class RootStorage(Storage):
  def __init__(self):
    super().__init__(None, None)
  
  def _bubble(self, key, value):
    # bubbles stop here
    self._try_responders(key, value)
    self._final(self._cache)
    pass
  
  def _final(self, value):
    # final value reported here
    pass
















class TestStorage(RootStorage):
  def __init__(self):
    super().__init__()
    self.static = Storage(self, 'static')
  
  def _final(self, value):
    pass

# some definitions and declarations
FAIL = Exception('test failed')
root_flag = None
static_flag = None

# ensure fields can be set
def test_set():
  s = TestStorage()
  s.field = 0

# ensure fields can be gotten after setting
def test_get():
  s = TestStorage()
  s.field = 3
  val = s.field

# ensure fields which aren't set 
def test_get_invalid():
  s = TestStorage()
  try:
    val = s.field
  except KeyError:
    return
  raise FAIL

# ensure that the value gotten is the one that was set
def test_access():
  val = 5
  s = TestStorage()
  s.field = val
  assert(s.field == val)

# test responders
def test_responders():
  global root_flag
  global static_flag

  static_val = 'a new thing'

  root_flag = None
  static_flag = None

  def root_responder(value):
    global root_flag
    root_flag = True
  
  def static_responder(value):
    global static_flag
    static_flag = value
  
  s = TestStorage()
  s._register(root_responder, 'static')
  s._register(static_responder, 'static.field')

  assert(len(s._responders) == 1)
  assert(len(s.static._responders) == 1)

  s.static.field = static_val

  assert(root_flag)
  assert(static_flag == static_val)

  s._deregister(root_responder, 'static')
  s._deregister(static_responder, 'static.field')

  assert(len(s._responders) == 0)
  assert(len(s.static._responders) == 0)










test_set()
test_get()
test_get_invalid()
test_access()
test_responders()

print('all test completed successfully!')


class PWConfig(Storage):
  def __init__(self, base, key):
    super().__init__(base, key)
    self.text = 'default'
    self.type = 'wpa2'


class NetConfig(Storage):
  def __init__(self, base, key):
    super().__init__(base, key)
    self.pw = PWConfig(self, 'pw')


class Config(RootStorage):
  def __init__(self):
    super().__init__()
    self.net = NetConfig(self, 'net')


c = Config()
c._register(lambda v: print(f'changed to {v}'), 'net.pw.type')
