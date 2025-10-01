# -*- coding: utf-8 -*-
"""Create Composite node for render on farm."""
import openpype.hosts.harmony.api as harmony
from openpype.hosts.harmony.api import plugin
from openpype.pipeline.context_tools import get_current_context, get_current_project_name


class CreateFarmRender(plugin.Creator):
    """Composite node for publishing renders."""

    name = "renderDefault"
    label = "Render on Farm"
    family = "renderFarm"
    node_type = "WRITE"

    def __init__(self, *args, **kwargs):
        """Constructor."""
        super(CreateFarmRender, self).__init__(*args, **kwargs)
    def context_png_check(self):
        """Check if the current context is requires a mov or a png seq."""
        project = get_current_project_name()
        context = get_current_context()
        if project.lower() == "horrible_science":
            if "animation" in context["task_name"].lower():
                return 1
        if "compositing" in context["task_name"].lower():
            return 1
        return 0

    def setup_node(self, node):
        """Set render node."""
        path = "render/{0}/{0}.".format(node.split("/")[-1])
        render_type = self.context_png_check()
        harmony.send(
            {
                "function": f"PypeHarmony.Creators.CreateRender.create",
                "args": [node, path, render_type]
            })
        harmony.send(
            {
                "function": f"PypeHarmony.color",
                "args": [[0.9, 0.75, 0.3, 1.0]]
            }
        )
