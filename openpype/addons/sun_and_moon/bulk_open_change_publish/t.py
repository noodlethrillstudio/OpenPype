import csv
import re

from openpype.lib import ApplicationManager
from time import sleep
from pathlib import Path


def get_episode(shot):

    if re.search("ep101",shot):
        episodeNumber = "101"
        episodeName = "ep101_shots_GARD"
    elif re.search("ep102", shot):
        episodeNumber = "102"
        episodeName = "ep102_shots_PUNT"
    elif re.search("ep103", shot):
        episodeNumber = "103"
        episodeName = "ep103_shots_CINE"
    elif re.search("ep109", shot):
        episodeNumber = "109"
        episodeName = "ep109_shots_LHOU"
    elif re.search("ep104", shot):
        episodeNumber = "104"
        episodeName = "ep104_shots_LIBR"
    elif re.search("ep105", shot):
        episodeNumber = "105"
        episodeName = "ep105_shots_PIZZ"
    elif re.search("ep106", shot):
        episodeNumber = "106"
        episodeName = "ep106_shots_BABY"
    elif re.search("ep107", shot):
        episodeNumber = "107"
        episodeName = "ep107_shots_BAKE"
    else:
        return None
    return episodeNumber,episodeName

def get_zip_path(asset, task, project):
    episodeNumber,episodeName = get_episode(asset)
    if episodeName == None or episodeNumber == None:
        return None
    dir = Path(f"D:/SynologyDrive/Duck_and_Frog/shots/{episodeName}/ep{episodeNumber}_sc01/{asset}/work/{task}/")
    print(f"dir:{dir}")
    version_pattern = re.compile(r'_v(\d+)', re.IGNORECASE)
    zips = list(dir.glob("*.zip"))

    if not zips:
        print("no zip dir found")
        return None

    def get_version(zip_path):
        match = version_pattern.search(zip_path.stem)
        return int(match.group(1)) if match else -1

    latest_zip = max(zips, key=get_version)
    path  = dir/latest_zip
    print(path)
    if not path.exists():
        return None
    with open(path, "rb") as f:
        b = f.read(1)
    if not b:
        sleep(60)
        print("Synology issue, retrying")
        get_zip_path(asset, task, project)
    return path

def launch_with_publish(harmony_script_path, shots, task_types):
    """Launch and publish the Harmony files using the Openpype gui."""

    """run compile first to set changes. THEN batch afterwards"""
    manager = ApplicationManager()
    print("manager init")
    if not shots:
        print("shots not found")
    for shot in shots:
        for task_type in task_types:
            print(fr"launching:{shot}, {task_type}")
            path = get_zip_path(shot, task_type, "Duck_and_Frog")
            print(f"path: {path}")
            if not path:
                print("no path found")
                break
            manager.launch(
                        "harmony/24",
                            app_args=[path, "-compile", harmony_script_path],
                            project_name="Duck_and_Frog",
                            asset_name= shot,
                            task_name=task_type)
            print("compile launched, waiting 15s")
            sleep(15)
            print("launching publish")
            manager.launch(
                "harmony/24",
                            app_args=[path, "-publish"],
                            project_name="Duck_and_Frog",
                            asset_name= shot,
                            task_name=task_type)
            print("batch launched, returning")


def launch_without_publish(harmony_script_path, shots, batch=True, task_types=["Compositing"] ):
    """Launch the Harmony files without using the Openpype gui. Instead, use -batch and -compile to make a change and render the scenes."""
    if batch:
        print("batch found")
        """run compile first to set changes. THEN batch afterwards"""
        manager = ApplicationManager()
        print("manager init")
        if not shots:
            print("shots not found")
        for shot in shots:
            for task_type in task_types:
                print(fr"launching:{shot}, {task_type}")
                path = get_zip_path(shot, task_type, "Duck_and_Frog")
                print(f"path: {path}")
                if not path:
                    print("no path found")
                    break
                manager.launch(
                            "harmony/24",
                                app_args=[path, "-compile", harmony_script_path],
                                project_name="Duck_and_Frog",
                                asset_name= shot,
                                task_name=task_type)
                print("compile launched, waiting 60s")
                sleep(15)
                print("launching batch")
                manager.launch(
                    "harmony/24",
                                app_args=[path, "-batch"],
                                project_name="Duck_and_Frog",
                                asset_name= shot,
                                task_name=task_type)
                print("batch launched, returning")


    elif not batch:
        "run compile script without rendering write nodes"
        manager = ApplicationManager()
        for shot in shots:
            for task_type in task_types:
                path  = get_zip_path(shot, task_type, "Duck_and_Frog")
                manager.launch(
                            "harmony/24",
                                app_args=[path, "-compile", harmony_script_path],
                                project_name="Duck_and_Frog",
                                asset_name= shot,
                                task_name=task_type)

def create_shot_array_from_csv(path):
    """Create array from shotlist CSV, where column is 'shots'."""
    try:
        with open(path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            csv_data = [row for row in reader]
            shots = [row[0] for row in csv_data if row]
        #print("Detected columns:", reader.fieldnames)
        return shots
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return []

#launch_without_publish("C:/Users/will_sunandmoonstudi/LatestOpenpypeBuild/OpenPype/openpype/addons/sun_and_moon/bulk_open_change_publish/compRender.js", create_shot_array_from_csv("C:/Users/will_sunandmoonstudi/Downloads/112.csv"), batch=True, task_types=["Animation"] )
launch_with_publish("C:/Users/will_sunandmoonstudi/LatestOpenpypeBuild/OpenPype/openpype/addons/sun_and_moon/bulk_open_change_publish/112ColourChange.js", create_shot_array_from_csv("C:/Users/will_sunandmoonstudi/Downloads/112.csv"), batch=True, task_types=["Animation"] )
