from .dotpath import DotPath

class Storage:
  """
  goals:
  * self-managing: updates to data should be immediately valid
  * fast access: reads should be quick
  * minimal dynamic memory usage: read/write operations should not generate excess objects
  * respondable: easy to register callbacks for when a field is updated
  * configuration-less: easy to create / modify the heirarchy of data
  * extendable: easy to add additional functionality using inheritance
  """
  
  def __init__(self, base, key, value):
    object.__setattr__(self, '_base', base)       # base storage object or None if root
    object.__setattr__(self, '_key', key)         # key of this storage within its base
    object.__setattr__(self, '_responders', {})   # responders for keys within this storage
    object.__setattr__(self, '_storage', {})      # sub level storage objects
    object.__setattr__(self, '_cache', {})        # plain-data cache of this storage

    # handle initial value if present
    if value is not None:
      assert(isinstance(value, dict))
      for k, v in value.items():
        self.__setattr__(k, v)
    
    # signal final form upon creation
    self._final(self._cache)

  def __setattr__(self, key, value):
    self._cache[key] = value
    self._update_storage(key, value)
    self._bubble(key, value)

  def __getattr__(self, key):
    return self._storage[key] if key in self._storage else self._cache[key]

  def __repr__(self):
    return str(self._cache)

  def _update_storage(self, key, value):
    if(isinstance(value, dict)):
      try:
        self._storage[key]
        for k, v in value.items():
          object.__setattr__(self._storage[key], k) 
      except KeyError:
        self._storage[key] = Storage(self, key, value)
    else:
      if key in self._storage:
        del self._storage[key]
  
  def _bubble(self, key, value):
    self._cache[key] = value
    self._try_responders(key, value)
    if self._base is not None:
      self._base._bubble(self._key, self._cache)
    else:
      self._final(self._cache)
  
  def _final(self, value):
    # final value reported here
    pass

  def _try_responders(self, key, value):
    try:
      for responder in self._responders[key]:
        responder(value)
    except KeyError:
      pass

  def _register(self, responder, path):
    p = DotPath(path)
    if p.is_final:
      try:
        self._responders[p.root].append(responder)
      except KeyError:
        self._responders[p.root] = [responder]
    else:
      self._storage[p.root]._register(responder, p.branch)
      
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
      self._storage[p.root]._deregister(responder, p.branch)
    pass



class RootStorage(Storage):
  """
  storage which terminates the chain by setting the base to None
  typically the best choice for parent of child classes
  allows for an initial value upon creation
  """
  def __init__(self, value=None):
    super().__init__(None, None, value)
