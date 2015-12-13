import sys, os 
import time
import csv
import couchdb
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

"""
Watch dog script.  This is designed to watch a directory
and look for new items being created.  When a new item is
created, the script finds the largest file in the direcotry
and uploads it to a CouchDB instance.  The file is then
deleted.

"""

def get_largest_file(file_path):
    """Get the largest file in a directory"""
    lg_file_size = 0
    lg_file = ""
    for item in os.listdir(file_path):
        item = os.path.join(file_path, item)
        f_size = os.path.getsize(item)
        if f_size > lg_file_size:
            lg_file_size = f_size
            lg_file = item

    return lg_file

def send_to_db(csv_file):
    """Send file to a database"""
    # If your CouchDB server is running elsewhere, set it up like this:
    #couch = couchdb.Server('http://127.0.0.1:5983/')
    couch = couchdb.Server('http://127.0.0.1:5984/')
    
    # select database
    #db = couch['flight_mon_db']
    db = couch['test_flight_mon']

    csvcont = csv.DictReader(open(csv_file, 'r'), delimiter=',')
    datas = [cont for cont in csvcont]

    for data in datas:
        db.save(data)



class flightHandler(FileSystemEventHandler):

    def on_created(self, event):
        path = os.path.split(event.src_path)[0]
        print path

        if len(os.listdir(path)) > 1:
            # find largest file
            data = get_largest_file(path)

            # send to db
            send_to_db(data)

            # remove file
            #os.remove(data)
        else:
            pass
            

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    event_handler = flightHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()