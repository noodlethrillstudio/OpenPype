import csv
import re

from sys import platform
from pathlib import Path
from time import sleep

from openpype.tools.pyblish_pype.window import Window
from openpype.tools.pyblish_pype import control
from openpype.tools.pyblish_pype.app import show, application
from openpype.lib import ApplicationManager

class BatchRender:
    def __init__(self, project = None, task_types = [] ):
        self.assets = []
        self.harmony_script_path = None
        self.project = project
        self.task_types = task_types
        self.episode_name = None
        self.asset_type = None

        self.root = None
        if platform =="darwin":
            self.root = "/Users/sunandmoon/SynologyDrive-sunandmoon/"
        elif platform=="win32":
            self.root= "D:/SynologyDrive/"

    def launch_with_publish(self, task_types):
        self.publish = True
        self.saveas = False
        self.window = Window(self)
        self.window.show()

    def launch_with_saveas(self, task_types):
        self.publish = False
        self.saveas = True
        self.window = Window(self)
        self.window.show()

    def _get_episode(self, asset):
        re.compile(r'ep(\d+))')
        if self.episode_name:
            episode_number = re.match(re.compile(r'ep(\d+))'), self.episode_name).group(1)
        else:
            return None
        return episode_number

    def _get_zip_path(self,asset, task, project):
        episode_number = self._get_episode(asset)

        root = Path(self.root)

        if episode_number == None:
            return None

        if self.asset_type == "shots":
            dir = root/project/self.asset_type/self.episode_name/"ep"+{episode_number}+"_sc01"/asset/"work"/task
        elif self.asset_type in ["0_ch","1_lc", "2_pr"]:
            dir = root/project/"assets"/self.asset_type/asset/"work"/task

        print(dir)
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
            self._get_zip_path(asset, task, project)
        return path

    def launch_harmony_without_publish(self, episode_name,asset_type, batch=True, ):
        """Launch the Harmony files without using the Openpype gui. Instead, use -batch and -compile to make a change and render the scenes."""
        project = self.project
        self.episode_name = episode_name
        assets = self.assets
        if batch:
            print("batch found")
            """run compile first to set changes. THEN batch afterwards"""
            manager = ApplicationManager()
            if not assets:
                print("assets not found")
            for asset in assets:
                for task_type in self.task_types:
                    path = self._get_zip_path(asset, task_type, project)
                    if not path:
                        print("no path found")
                        break

                    manager.launch(
                                "harmony/24",
                                    app_args=[path,"-compile", self.harmony_script_path],
                                    project_name=project,
                                    asset_name= asset,
                                    task_name=task_type)
                    print("compile launched, waiting 15s")
                    sleep(15)
                    print("launching batch")

                    manager.launch(
                        "harmony/24",
                                    app_args=[path,"-batch"],
                                    project_name=project,
                                    asset_name= asset,
                                    task_name=task_type)
                    print("batch launched, returning")
                    return

        elif not batch:
            "run compile script without rendering write nodes"
            manager = ApplicationManager()
            for asset in self.assets:
                for task_type in self.task_types:
                    path = self.get_zip_path(asset, task_type, project)
                    manager.launch(
                                "harmony/24",
                                    app_args=[path,"-compile", self.harmony_script_path],
                                    project_name=project,
                                    asset_name= asset,
                                    task_name=task_type)

    def create_asset_array_from_csv(self):
        """create array from assetlist csv, Where column is 'assets'"""
        with open(self.csv_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            csv_data = [row for row in reader]
        self.assets = [row['assets'] for row in csv_data if 'assets' in row]



def main():
    print("main running")
    render = BatchRender(project="Duck_and_Frog", task_types=["Compositing"])
    print("render initiated")
    render.harmony_script_path = "C:/Users/will_sunandmoonstudi/LatestOpenpypeBuild/OpenPype/openpype/addons/sun_and_moon/bulk_open_change_publish/compRender.js"
    print("path set")
    render.create_asset_array_from_csv(fr"C:\Users\will_sunandmoonstudi\Downloads\101.csv")
    print("csv found")
    render.launch_harmony_without_publish()
    print("launch method called")
main()


def autopublish():
    """This is the editors autopublish script. Please change the following variables to render an episode:"""

    project = "Duck_and_Frog" #Change if needed
    task_types =["Compositing"] #Change if needed

    task = BatchRender(project,task_types)

    harmony_script_path = fr"{task.root}/Duck_and_Frog/resources/rendering/comp_batch_harmony/compRender.js"

# script_path = rf"C:\Users\will_sunandmoonstudi\LatestOpenpypeBuild\OpenPype\openpype\addons\sun_and_moon\bulk_open_change_publish\compRender.js"
