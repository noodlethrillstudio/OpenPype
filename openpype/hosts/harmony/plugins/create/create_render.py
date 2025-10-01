# -*- coding: utf-8 -*-
"""Create render node."""
import openpype.hosts.harmony.api as harmony
from openpype.hosts.harmony.api import plugin
from openpype.pipeline.context_tools import get_current_context, get_current_project_name


class CreateRender(plugin.Creator):
    """Composite node for publishing renders."""

    name = "renderDefault"
    label = "Render"
    family = "render"
    node_type = "WRITE"

    def __init__(self, *args, **kwargs):
        """Constructor."""
        super(CreateRender, self).__init__(*args, **kwargs)
    def context_png_check(self):
        """Check if the current context is requires a mov or a png seq."""
        context = get_current_context()
        project = get_current_project_name()
        if project.lower() == "horrible_science":
            if "animation" in context["task_name"].lower():
                return 1
        if "compositing" in context["task_name"].lower():
            return 1
        return 0

    def setup_node(self, node):
        """Set render node."""
        self_name = self.__class__.__name__
        path = "render/{0}/{0}.".format(node.split("/")[-1])
        render_type = self.context_png_check()
        harmony.send(
            {
                "function": f"PypeHarmony.Creators.{self_name}.create",
                "args": [node, path, render_type]
            })
