from openpype.lib import ApplicationManager

manager = ApplicationManager()
manager.launch(
            "harmony/24",
                app_args=["-compile", "C:/Users/will_sunandmoonstudi/LatestOpenpypeBuild/OpenPype/openpype/addons/sun_and_moon/bulk_open_change_publish/test.js"],
                project_name="Duck_and_Frog",
                asset_name="test",
                task_name="Animation"
            )
