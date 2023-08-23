###### *Alpha Preview 0.0.0*
# baseofdata
Lightweight database system

***Upstream Version, Do Not Use in Production***
## Installing from Release
```
$ wget https://github.com/islekcaganmert/baseofdata/releases/download/Preview/baseofdata-0.0.1-py3-none-any.whl
$ python3 -m pip install ./baseofdata-0.0.1-py3-none-any.whl
```
## Building
```
$ git clone https://github.com/islekcaganmert/baseofdata
$ cd baseofdata
$ make build
$ make install
```
## Simple Example

```
from baseofdata import Data

db = Data('demo.Data')

db.create({
    'id': 'Integer',
    'name': 'String',
    'GPA': 'Float',
    'Available': 'Boolean'
})

db.add(id=1, name='Cagan Mert ISLEK', GPA=4.0, Available=True)
db.add(id=2, name='Cagan Mert ISLEK', GPA=4.0, Available=True)

db.remove(0)

db.edit(__id__=0, id=1, Available=False)

print(db.get(name='Cagan Mert ISLEK', GPA=4.0, Available=True))
```
## Links
- Documentation: *Soon*
- PyPI Releases: *Soon*
- Source Code: https://github.com/islekcaganmert/baseofdata/
- Issue Tracker: https://github.com/islekcaganmert/baseofdata/issues/
- Community: https://hereus.pythonanywhere.com/communities/baseofdata