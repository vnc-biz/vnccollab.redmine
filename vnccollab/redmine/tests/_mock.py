import dateutil.parser
from pyactiveresource.activeresource import ActiveResource

res = [
    {'status': None, 
    'priority': None, 
    'description': u'some description 1', 
    'parent': None, 
    'author': None, 
    'raw_is_dict': False, 
    'due_date': None, 
    'start_date': dateutil.parser.parse('2014/03/12 00:00:00 GMT+0'), 
    'project': None, 
    'created_on': dateutil.parser.parse('2014/03/12 10:48:49 GMT+1'), 
    'tracker': None, 
    'updated_on': dateutil.parser.parse('2014/03/17 19:47:37 GMT+1'), 
    'fixed_version': u'', 
    'assigned_to': None, 
    'estimated_hours': -1.0, 
    'journals': [], 
    'id': u'10560', 
    'done_ratio': 0.0, 
    'subject': u'Some subject 1'},
    {'status': None, 
    'priority': None, 
    'description': u'some description 2', 
    'parent': None, 
    'author': None, 
    'raw_is_dict': False, 
    'due_date': None, 
    'start_date': dateutil.parser.parse('2014/03/12 00:00:00 GMT+0'), 
    'project': None, 
    'created_on': dateutil.parser.parse('2014/03/12 10:48:49 GMT+1'), 
    'tracker': None, 
    'updated_on': dateutil.parser.parse('2014/03/17 19:47:37 GMT+1'), 
    'fixed_version': u'', 
    'assigned_to': None, 
    'estimated_hours': -1.0, 
    'journals': [], 
    'id': u'10560', 
    'done_ratio': 0.0, 
    'subject': u'Some subject 2'},]

usr = {'last_login_on': '2014-03-20T00:07:09+01:00',
       'firstname': 'Marcin',
       'lastname': 'Staniszczak',
       'created_on': dateutil.parser.parse('2013-03-07T13:33:10+01:00'),
       'mail': 'marcin.staniszczak@vnc.biz',
       'id': '202',
       'custom_fields': []}


class Fake(object):
    def __init__(self, **entries): 
        self.__dict__.update(entries)
        self._raw = entries

    def to_dict(self):
        return self._raw

    def __getitem__(self, key):
        return self._raw[key]


@classmethod
def find(cls, id_=None, from_=None, **kwargs):
    if cls._singular == 'user':
        return Fake(**usr)

    return [Fake(**r) for r in res]


@classmethod
def get(cls, id_=None, from_=None, **kwargs):
    if cls._singular == 'user':
        return Fake(**usr)

    return Fake(**res[0])


def initialize():
    ActiveResource.find = find
    ActiveResource.get = get