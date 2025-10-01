import os
from openpype.modules import OpenPypeModule, IHostAddon

STORYBOARDPRO_HOST_DIR = os.path.dirname(os.path.abspath(__file__))


class StoryboardProAddon(OpenPypeModule, IHostAddon):
    name = "storyboardpro"
    host_name = "storyboardpro"

    def initialize(self, module_settings):
        self.enabled = True

    def add_implementation_envs(self, env, _app):
        """Modify environments to contain all required for implementation."""

        defaults = {
            "OPENPYPE_LOG_NO_COLORS": "True"
        }
        for key, value in defaults.items():
            if not env.get(key):
                env[key] = value

    def get_workfile_extensions(self):
        return [".sbpz"]
