import inotify.adapters
import subprocess
import os

i=inotify.adapters.Inotify()
filepath="/home/pi/work/data"
serverpath="generalmine@95.208.136.144:work/data"
i.add_watch(filepath)

try:
    for event in i.event_gen():
        if event is not None:
            (header, type_names, watch_path, filename) = event
            if "IN_CLOSE_WRITE" in type_names:
                print("File created...")
                subprocess.call(["scp", filepath + "/" + filename, serverpath])
                print("File uploaded")
                os.remove(filepath+"/"+filename)
                print("File deleted")
finally:
    i.remove_watch(filepath)
