import os
import subprocess

import inotify.adapters

i = inotify.adapters.Inotify()
filepath = "/home/pi/work/data"  # config file Path
serverpath = "generalmine@95.208.136.144:work/data"  # config Habitat Server
i.add_watch(filepath)  # subscribe to server event in folder


try:
    for event in i.event_gen():
        if event is not None:  # if a new event exists
            (header, type_names, watch_path, filename) = event
            if (
                "IN_CLOSE_WRITE" in type_names
            ):  # if new closed file in subscribed folder
                print("File created...")
                subprocess.call(
                    ["scp", filepath + "/" + filename, serverpath]
                )  # push file to Habitat Server
                print("File uploaded")
                os.remove(
                    filepath + "/" + filename
                )  # remove file from pseudo-satellites
                print("File deleted")
finally:
    i.remove_watch(filepath)  # reset watch
