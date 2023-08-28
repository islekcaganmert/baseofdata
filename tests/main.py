from baseofdata import Data

db = Data('demo.Data')
db.autosync = True

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