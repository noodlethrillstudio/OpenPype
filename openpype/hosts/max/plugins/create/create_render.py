# -*- coding: utf-8 -*-
"""Creator plugin for creating camera."""
from openpype.hosts.max.api import plugin
from openpype.lib import (
    TextDef,
    BoolDef,
    NumberDef,
)
from openpype.pipeline import CreatedInstance
from openpype.hosts.max.api.lib_rendersettings import RenderSettings


class CreateRender(plugin.MaxCreator):
    identifier = "io.openpype.creators.max.render"
    label = "Render"
    family = "maxrender"
    icon = "gear"

    def apply_settings(self, project_settings, system_settings):
        plugin_settings = (
            project_settings["deadline"]["publish"]["MaxSubmitDeadline"]
        )
        self.use_published = plugin_settings["use_published"]
        self.priority = plugin_settings["priority"]
        self.chunkSize = plugin_settings["chunk_size"]
        self.group = plugin_settings["group"]
        self.deadline_pool = plugin_settings["deadline_pool"]
        self.deadline_pool_secondary = plugin_settings["deadline_pool_secondary"]

    def create(self, subset_name, instance_data, pre_create_data):
        from pymxs import runtime as rt
        sel_obj = list(rt.selection)
        instance = super(CreateRender, self).create(
            subset_name,
            instance_data,
            pre_create_data)  # type: CreatedInstance
        container_name = instance.data.get("instance_node")
        container = rt.getNodeByName(container_name)
        # TODO: Disable "Add to Containers?" Panel
        # parent the selected cameras into the container
        for obj in sel_obj:
            obj.parent = container
        # for additional work on the node:
        # instance_node = rt.getNodeByName(instance.get("instance_node"))

        # set viewport camera for rendering(mandatory for deadline)
        RenderSettings().set_render_camera(sel_obj)
        # set output paths for rendering(mandatory for deadline)
        RenderSettings().render_output(container_name)

    def get_instance_attr_defs(self):
        return [
            BoolDef("use_published",
                    default=self.use_published,
                    label="Use Published Scene"),

            NumberDef("priority",
                      minimum=1,
                      maximum=250,
                      decimals=0,
                      default=self.priority,
                      label="Priority"),

            NumberDef("chunkSize",
                      minimum=1,
                      maximum=50,
                      decimals=0,
                      default=self.chunkSize,
                      label="Chunk Size"),

            TextDef("group",
                    default=self.group,
                    label="Group Name"),

            TextDef("deadline_pool",
                    default=self.deadline_pool,
                    label="Deadline Pool"),

            TextDef("deadline_pool_secondary",
                    default=self.deadline_pool_secondary,
                    label="Deadline Pool Secondary")
        ]

    def get_pre_create_attr_defs(self):
        return self.get_instance_attr_defs()
