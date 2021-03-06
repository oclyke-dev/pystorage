from storage import RootStorage

root_flag = None
static_flag = None
FAIL = Exception('test failed')

class TestStorage(RootStorage):
  pass

def test_assignment():
  s = TestStorage()
  s.field = '42'

# ensure fields can be set
def test_set():
  s = TestStorage()
  s.field = 0

# ensure fields can be set
def test_item_assignment():
  s = TestStorage()
  s['field'] = 0

# ensure dicts can be set
def test_set_dict():
  s = TestStorage()
  s.field = {'arbitrary': 'keys'}

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

# ensure fields can be cleared
def test_empty_dict_overwrite():
  s = TestStorage()
  nested = {'deep': 42}
  s.nested = nested

  assert(s.nested['deep'] == nested['deep'])

  # try to set the nested value back to empty dict
  s.nested = {}

  passing = False
  try:
    s.nested.deep
  except KeyError:
    passing = True # expect the above operation to fail

  if not passing:
    raise FAIL

  s['field'] = 0
      
# ensure fields can be deleted
def test_field_del():
  s = TestStorage()
  nested = {'deep': 42}
  s.nested = nested

  assert(s.nested['deep'] == nested['deep'])
  del s.nested['deep']

  passing = False
  try:
    s.nested.deep
  except KeyError:
    passing = True
  
  if not passing:
    raise FAIL

# ensure fields can be deleted
def test_re_set_dict():
  s = TestStorage()
  nested = {'deep': 42}
  second = {'key': 'value'}

  s.nested = nested
  assert(s.nested['deep'] == nested['deep'])

  s.nested = second
  assert(s.nested['key'] == second['key'])

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
  s.static = {}
  s._register(root_responder, 'static')
  s._register(static_responder, 'static.field')

  s.static.field = static_val

  assert(root_flag)
  assert(static_flag == static_val)

  s._deregister(root_responder, 'static')
  s._deregister(static_responder, 'static.field')
