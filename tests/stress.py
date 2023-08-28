from baseofdata import Data
from random import randint
from time import sleep
from datetime import datetime
import threading

db = Data('demo.Data')

db.create({'num':'String'})

def db_add_proc(): db.add(num=str(randint(10000,99999)))

start_time = datetime.utcnow()
for i in range(10000):
    db_add = threading.Thread(target=db_add_proc)
    db_add.start()
    while db_add.is_alive():
        if (datetime.utcnow()-start_time).total_seconds() < 10: print(' '+str((i/10000)*100).split('.')[0]+'%     '+str(datetime.utcnow()-start_time).split('.')[0]+' passed', end='\r',flush=True) #print('*',end='', flush=True)
        else:
            graph = ''
            try:
                for k in range(int(str(i/((datetime.utcnow()-start_time).total_seconds()/60)).split('.')[0][:-2])): graph+='|'
            except: pass
            for k in range(80-int(str(i/((datetime.utcnow()-start_time).total_seconds()/60)).split('.')[0][:-2])): graph+=' '
            print(' '+str((i/10000)*100).split('.')[0]+'%     '+str(datetime.utcnow()-start_time).split('.')[0]+' passed     '+str(i/((datetime.utcnow()-start_time).total_seconds()/60)).split('.')[0]+' column/min     '+str(((10000-i)*(10000/i))/(i/((datetime.utcnow()-start_time).total_seconds()/60))).split('.')[0]+' minute remaining     '+graph, end='\r',flush=True) #print('*',end='', flush=True)

print('Done in '+str(datetime.utcnow()-start_time).split('.')[0])

print('\nFetching database...',end=' ', flush=True)
db.fetch()
print('DONE!')
sleep(1)

for data in db.data:
    print(data['num'])