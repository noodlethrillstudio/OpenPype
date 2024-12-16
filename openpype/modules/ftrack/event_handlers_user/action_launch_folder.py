import subprocess
import logging
import os
import collections
import copy

from sys import platform
from openpype_modules.ftrack.lib import BaseAction, statics_icon
from openpype.pipeline import Anatomy
from openpype.lib import Logger

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class LaunchFolder(BaseAction):

    label = 'Launch Folder'
    identifier = 'launch.folder'
    description = 'launches associated drive folder'
    icon = statics_icon("ftrack", "action_icons", "sunandmoon.png")



    def discover(self, session, entities, event):

        """Return True when single entity is selected."""
        ''' Validation '''
        valid = True

        # Check for multiple selection.
        if len(entities) > 1:
            valid = False


        return valid

    def launch(self, session, entities, event):
        entity = entities[0]
        is_asset = False
        is_task = False

        if entities[0].entity_type == "AssetVersion":

            self.log.info("Is AssetVersion")
            is_asset = True

        elif entities[0].entity_type == "Task":

            self.log.info("Is Task")
            is_task = True
        elif entities[0].entity_type != "AssetVersion" and entities[0].entity_type != "Task":
            self.log.info("Is Folder")



        project_entity = self.get_project_from_entity(entities[0])

        project_name = project_entity["full_name"]
        project_code = project_entity["name"]

        if is_task:
            task_types = session.query("select id, name from Type").all()
            task_type_names_by_id = {
                task_type["id"]: task_type["name"]
                for task_type in task_types
            }

        if is_asset:
            task_types = session.query("select id, name from Type").all()
            task_type_names_by_id = {
                task_type["id"]: task_type["name"]
                for task_type in task_types
            }

        anatomy = Anatomy(project_name)

        work_keys = ["work", "folder"]
        work_template = anatomy.templates
        for key in work_keys:
            work_template = work_template[key]

        publish_keys = ["publish", "folder"]
        publish_template = anatomy.templates
        for key in publish_keys:
            publish_template = publish_template[key]

        project_data = {
            "project": {
                "name": project_name,
                "code": project_code
            }
        }

        hierarchy_names = []
        if is_asset:
            parent_entity= entity["task"]["parent"]
        elif is_task:
            parent_entity = entity["parent"]
        elif not is_asset and not is_task:
            parent_entity = entity

        parent_data = copy.deepcopy(project_data)

        while parent_entity.get("parent"):
            parent_entity = parent_entity["parent"]

            if parent_entity.entity_type.lower() == "project":
                break
            hierarchy_names.append(parent_entity["name"])

        hierarchy = "/".join(reversed(hierarchy_names))
        self.log.info(f"Hierarchy: {hierarchy}")

        if is_task:
            if project_name == "Duck_and_Frog"  and "editorial" in hierarchy_names:
                editorial_template = self.get_editorial_folders_DF(entity)
                if editorial_template: editorial_override = True
            elif project_name == "Maddie_and_Triggs" and "editorial" in hierarchy_names:
                editorial_template = self.get_editorial_folders_MT(entity)
                if editorial_template: editorial_override = True
            

        if not is_asset:
            parent_entity = entity["parent"]

        if is_task:
            parent_name = hierarchy_names[0]
            parent_data.update({
                #here, asset needs to be the parent of the task you've selected.
                # For a design task, it should be the shot
                "asset": parent_entity["name"],
                "hierarchy": hierarchy,
                "parent": parent_name
            })

        elif is_asset:
            # Update data with hierarchy
            parent_data.update({
                "asset": entity["task"]["parent"]["name"],
                "hierarchy": hierarchy,
                "parent": hierarchy_names[-1] if hierarchy_names else project_name,
                "family": entity["asset"]["type"]["name"],
                "subset": entity["asset"]["name"],
                "version": entity["version"]
            })
            self.log.info(f"Parent data: {parent_data}")
        elif not is_asset and not is_task:
            # Update data with hierarchy
            project_data.update({
                "asset": entity["name"],
                "hierarchy": hierarchy,
                "parent": hierarchy_names[-1] if hierarchy_names else project_name
            })

        if is_asset:
            task_type_id = entity["task"]["type_id"]
            task_type_name = task_type_names_by_id[task_type_id]
            task_data = copy.deepcopy(parent_data)
            task_data["task"] = {
                "name": entity["task"]["name"],
                "type": task_type_name,
                }
            self.log.info(f"Task data: {task_data}")
            publish_path = self.compute_template(anatomy, task_data, publish_keys)

            path = publish_path
          
        elif is_task and editorial_override == False:
            self.log.info("Is task, work path used")
            task_type_id = entity["type_id"]
            task_type_name = task_type_names_by_id[task_type_id]
            task_data = copy.deepcopy(parent_data)

            task_data["task"] = {
                "name": entity["name"],
                "type": task_type_name
                }
            self.log.info(f"Task data: {task_data}")
            work_path = self.compute_template(anatomy, task_data, work_keys)
            path = work_path
        
         
        elif is_task and editorial_override == True:
            self.log.info("Is task, work path used")
            task_type_id = entity["type_id"]
            task_type_name = task_type_names_by_id[task_type_id]
            task_data = copy.deepcopy(parent_data)

            task_data["task"] = {
                "name": entity["name"],
                "type": task_type_name
                }
            self.log.info(f"Task data: {task_data}")
            work_path = self.compute_template_folder(anatomy, task_data, work_keys)
            for key in editorial_template:
                work_path = work_path + "/" + editorial_template[key]

        elif not is_asset and not is_task:
            folder_path = self.compute_template_folder(anatomy, project_data, work_keys)
            path = folder_path


        self.log.info("Opening path:")


        self.log.info(path)
        if not os.path.exists(path):
            self.log.info("path does not exist")
            return {"success": False,
                    "message": "Path does not exist"}
        self.open_folder(path)

        return {
            "success": True,
            "message": "Opening folder"
        }

    def get_editorial_folders_DF(self, entity):
        ed_folder_template = {}
        if entity["name"] == "Script_Ready":
            ed_folder_template= {
                "task": "story",
                "subfolder": "Final Script"
            }
        elif entity["name"] == "Asset_Breakdown":
            ed_folder_template= {
                "task": "asset_breakdown"
            }
        elif entity["name"] == "Scene_Breakdown":
            ed_folder_template= {
                "task": "scene_breakdown",
            }
        elif entity["name"] == "Thumbnail_Animatic":
            ed_folder_template= {
                "task": "animatic",
                "subfolder": "thumbnail_animatic_workfiles"
            }
        elif entity["name"] == "Scratch_VO":
            ed_folder_template= {
                "task": "sound",
                "subfolder": "01_scratch"
            }
        elif entity["name"] == "Edit_Scratch_Sound":
            ed_folder_template= {
                "task": "edit",
                "subfolder": "edit_workfiles"
            }
        elif entity["name"] == "Animatic":
            ed_folder_template= {
                "task": "animatic",
                "subfolder": "animatic_workfiles"
            }
        elif entity["name"] == "VO_Record":
            ed_folder_template= {
                "task": "sound",
                "subfolder": "02_VO"
            }
        elif entity["name"] == "Edit_Animatic":
            ed_folder_template= {
                "task": "edit",
                "subfolder": "edit_workfiles"
            }
        elif entity["name"] == "Create_Shots":
            ed_folder_template= {
                "task": "edit",
                "subfolder": "edit_workfiles"
            }
        elif entity["name"] == "Sound":
            ed_folder_template= {
                "task": "sound",
            }
        elif entity["name"] == "Edit_Animation":
            ed_folder_template= {
                "task": "edit",
                "subfolder": "edit_workfiles"
            }
        elif entity["name"] == "Edit_Comp":
            ed_folder_template= {
                "task": "edit",
                "subfolder": "edit_workfiles"
            }
        return ed_folder_template
    
    def get_editorial_folders_MT(self, entity):
        ed_folder_template = {}
        if entity["name"] == "Story_Script":
            ed_folder_template= {
                "task": "story",
                "subfolder": "script"
            }
        elif entity["name"] == "VO_Script_Read":
            ed_folder_template= {
                "task": "sound"
            }
        elif entity["name"] == "Radioplay":
            ed_folder_template= {
                "task": "sound",
                "subfolder": "01_radioplay"
            }
        elif entity["name"] == "Asset_Breakdown":
            ed_folder_template= {
                "task": "asset_breakdown"
            }
        elif entity["name"] == "Animatic_Setup":
            ed_folder_template= {
                "task": "animatic"
            }
        elif entity["name"] == "Thumbnail_Animatic_A":
            ed_folder_template= {
                "task": "animatic",
                "subfolder": "thumbnail_animatic_workfiles"
            }
        elif entity["name"] == "Thumbnail_Animatic_B":
            ed_folder_template= {
                "task": "animatic",
                "subfolder": "thumbnail_animatic_workfiles"
            }
        elif entity["name"] == "Thumbnail_Animatic_C":
            ed_folder_template= {
                "task": "animatic",
                "subfolder": "thumbnail_animatic_workfiles"
            }
        elif entity["name"] == "Animatic_sc01":
            ed_folder_template= {
                "task": "animatic",
                "subfolder": "animatic_workfiles"
            }
        elif entity["name"] == "Animatic_sc02":
            ed_folder_template= {
                "task": "animatic",
                "subfolder": "animatic_workfiles"
            }
        elif entity["name"] == "Animatic_sc03":
            ed_folder_template= {
                "task": "animatic",
                "subfolder": "animatic_workfiles"
            }
        elif entity["name"] == "Animatic_sc04":
            ed_folder_template= {
                "task": "animatic",
                "subfolder": "animatic_workfiles"
            }
        elif entity["name"] == "Animatic_sc05":
            ed_folder_template= {
                "task": "animatic",
                "subfolder": "animatic_workfiles"
            }
        elif entity["name"] == "Animatic_sc06":
            ed_folder_template= {
                "task": "animatic",
                "subfolder": "animatic_workfiles"
            }

        elif entity["name"] == "VO_Record":
            ed_folder_template= {
                "task": "sound",
                "subfolder": "02_VO"
            }
        elif entity["name"] == "Edit_Animatic":
            ed_folder_template= {
                "task": "edit",
                "subfolder": "edit_workfiles"
            }
        elif entity["name"] == "Create_Shots":
            ed_folder_template= {
                "task": "edit",
                "subfolder": "edit_workfiles"
            }
        elif entity["name"] == "Sound_Music":
            ed_folder_template= {
                "task": "sound",
                "subfolder": "03_music"
            }
        elif entity["name"] == "Edit_Animation":
            ed_folder_template= {
                "task": "edit",
                "subfolder": "edit_workfiles"
            }
        elif entity["name"] == "Edit_Comp":
            ed_folder_template= {
                "task": "edit",
                "subfolder": "edit_workfiles"
            }
        return ed_folder_template



    def get_all_entities(
        self, session, entities, task_entities, other_entities
    ):
        if not entities:
            return

        no_task_entities = []
        for entity in entities:
            if entity.entity_type.lower() == "task":
                task_entities.append(entity)
            else:
                no_task_entities.append(entity)

        if not no_task_entities:
            return task_entities

        other_entities.extend(no_task_entities)

        no_task_entity_ids = [entity["id"] for entity in no_task_entities]
        next_entities = session.query((
            "select id, parent_id"
            " from TypedContext where parent_id in ({})"
        ).format(self.join_query_keys(no_task_entity_ids))).all()

        self.get_all_entities(
            session, next_entities, task_entities, other_entities
        )


    def compute_template(self, anatomy, data, anatomy_keys):
        filled_template = anatomy.format_all(data)
        for key in anatomy_keys:
            filled_template = filled_template[key]
            self.log.info(f"Filled template: {filled_template}")

        if filled_template.solved:
            return os.path.normpath(filled_template)

        self.log.warning(
            "Template \"{}\" was not fully filled \"{}\"".format(
                filled_template.template, filled_template
            )
        )
        return os.path.normpath(filled_template.split("{")[0])

    def compute_template_folder(self, anatomy, data, work_keys):
        filled_template = anatomy.format_all(data)
        for key in work_keys:
            filled_template = filled_template[key]

        #if filled_template.solved:
            #return os.path.normpath(filled_template)

        # self.log.warning(
        #     "Template \"{}\" was not fully filled \"{}\"".format(
        #         filled_template.template, filled_template
        #     )
        # )
        return os.path.normpath(filled_template.split("work")[0])

    def check_platform(self):
        if platform == "win32":
            return "win32"
        elif platform == "darwin":
            return "darwin"
        log.debug("Platform not found or not supported")
        return {"success": False,
                "message": "Platform not found or not supported"}

    def open_file(self, path):
        if self.check_platform() == "win32":
            if os.path.exists(path):
                subprocess.Popen(f'explorer /select,"{path}"')
                return
            elif not os.path.exists(path):
                log.debug("File location does not exist")
                return {'success': False,
                        'message': "File path connot be found, ensure file sharing drive is connected"}

        elif self.check_platform() == "darwin":
            if os.path.exists(path):
                subprocess.Popen('open','-R', path)
                return
            elif not os.path.exists(path):
                log.debug("File location does not exist")
                return {'success': False,
                        'message': "File path connot be found, ensure file sharing drive is connected"}


    def open_folder(self, path):
        if self.check_platform() == "win32":
            if os.path.exists(path):
                subprocess.Popen(f'explorer "{path}"')
                return
            elif not os.path.exists(path):
                log.debug("File location does not exist")
                return {'success': False,
                        'message': "File path connot be found, ensure file sharing drive is connected"}

        elif self.check_platform() == "darwin":
            if os.path.exists(path):
                subprocess.Popen(['open','-R', path])
                return
            elif not os.path.exists(path):
                log.debug("File location does not exist")
                return {'success': False,
                        'message': "File path connot be found, ensure file sharing drive is connected"}

def register(session):
    '''Register plugin. Called when used as an plugin.'''
    LaunchFolder(session).register()
