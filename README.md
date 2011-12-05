http://github.com/amccloud/redy/

Example
=======

From lamernews' <https://github.com/antirez/lamernews> user data structure.

```python
from datetime import datetime
import redy

class User(redy.Model):
    username = redy.AttributeField(indexed=True)
    password = redy.AttributeField()
    ctime = redy.DateTimeField(default=datetime.now)
    karma = redy.CounterField(default=1)
    about = redy.AttributeField()
    email = redy.AttributeField()
    auth = redy.AttributeField()
    apisecret = redy.AttributeField()
    flags = redy.AttributeField()
    karma_incr_time = redy.AttributeField()


user = User(
    username='amccloud',
    password='<hash>',
)

user.save()

print user.id
# >>> 1

print user.username
# >>> 'amccloud'

print user.ctime
# >>> '2011-12-04 02:31:12.092451'

print user.karma
# >>> 1

user.karma = 2
user.save()

print user.karma
# >>> 2
```