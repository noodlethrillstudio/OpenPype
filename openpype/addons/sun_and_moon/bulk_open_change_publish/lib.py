import os

from openpype.modules import OpenPypeModule
from openpype.lib import ApplicationManager
from openpype.lib.applications import ApplicationLaunchContext
from openpype.hosts.harmony.api.lib import(
    launch_zip_file
)

"""Run code from Ftrack action to get list of files to open, change and publish."""
# command args: Harmony<Edition> PathToScene/Scene.xstage -batch -compile PathToScript/Script.js

# so, additional args to tack onto normal application launch are: -batch -compile PathToScript/Script.js



# identify files

# identify pre launch hooks

# identify post launch hooks

# get change_script to run inside the file

# run pre launch hooks

# launch host headless

# run post launch hooks

# run change_script

# if not farm render node, create render node.

# publish farm render node and workfile.

# close file.

# loop


##:: C:\"Program Files (x86)\Toon Boom Animation\Toon Boom Harmony 24 Premium\win64\bin\HarmonyPremium.exe" "C:\Users\will_sunandmoonstudi\.avalon\harmony\DAF_test_Animation_v038\DAF_test_Animation_v038.xstage" -compile "C:\Users\will_sunandmoonstudi\LatestOpenpypeBuild\OpenPype\openpype\modules\sun_and_moon\bulk_open_change_publish\test.js"


"""@NOTE: Need to inject the script instead of using compile flag"""

class BulkApplicationManager(ApplicationManager):
    def create_launch_context(self, app_name, **data):
        """Prepare launch context for application.

        Args:
            app_name (str): Name of application that should be launched.
            **data (Any): Any additional data. Data may be used during

        Returns:
            ApplicationLaunchContext: Launch context for application.

        Raises:
            ApplicationNotFound: Application was not found by entered name.
        """

        app = self.applications.get(app_name)
        if not app:
            raise ApplicationNotFound(app_name)

        executable = app.find_executable()

        return BulkApplicationLaunchContext(
            app, executable, **data
        )

class BulkApplicationLaunchContext(ApplicationLaunchContext):
    script_path = "C:/Users/will_sunandmoonstudi/LatestOpenpypeBuild/OpenPype/openpype/addons/sun_and_moon/bulk_open_change_publish/test.js"
    def _run_process(self):
        # Windows and MacOS have easier process start
        low_platform = platform.system().lower()
        if low_platform in ("windows", "darwin"):
            self.launch_args = self.launch_args
            return subprocess.Popen(self.launch_args, **self.kwargs)

        # Linux uses mid process
        # - it is possible that the mid process executable is not
        #   available for this version of OpenPype in that case use standard
        #   launch
        launch_args = get_linux_launcher_args()
        if launch_args is None:
            return subprocess.Popen(self.launch_args, **self.kwargs)

        # Prepare data that will be passed to midprocess
        # - store arguments to a json and pass path to json as last argument
        # - pass environments to set
        app_env = self.kwargs.pop("env", {})
        json_data = {
            "args": self.launch_args,
            "env": app_env
        }
        if app_env:
            # Filter environments of subprocess
            self.kwargs["env"] = {
                key: value
                for key, value in os.environ.items()
                if key in app_env
            }

        # Create temp file
        json_temp = tempfile.NamedTemporaryFile(
            mode="w", prefix="op_app_args", suffix=".json", delete=False
        )
        json_temp.close()
        json_temp_filpath = json_temp.name
        with open(json_temp_filpath, "w") as stream:
            json.dump(json_data, stream)

        launch_args.append(json_temp_filpath)

        # Create mid-process which will launch application
        process = subprocess.Popen(launch_args, **self.kwargs)
        # Wait until the process finishes
        #   - This is important! The process would stay in "open" state.
        process.wait()
        # Remove the temp file
        os.remove(json_temp_filpath)
        # Return process which is already terminated
        return process
