import io
import csv
import logging
from openpype_modules.ftrack.lib import BaseAction, statics_icon
#from ftrack_action_handler import BaseAction
import ftrack_api


# session = ftrack_api.Session(
#     server_url='https://sun-moon-studios.ftrackapp.com',
#     api_key='MWExNTVjNTUtZjk0My00N2M3LTgxMjktYWQzMWM4MDE0NDNlOjpiMjc3OTQ2Ny00M2QzLTRiZjctOWEwNy00NWEzZGJmNTA4OGE',
#     api_user='will@sunandmoonstudios.co.uk',
#     auto_connect_event_hub=True
# )


RUN_AS_ACTION = True  # Set to False to run as an event listener.
UPDATE_LABELS = False  # Set to False to create comments instead.


class addNotesFromCsv(BaseAction):

    label = 'Add Notes from CSV'
    identifier = 'com.ftrack.recipes.add_notes_from_csv'
    description = 'Add notes to ftrack entities from csv spreadsheet'
    #icon = statics_icon("ftrack", "action_icons", "sunandmoon.png")


    def discover(self, session, entities, event):
        """Return True if selection is a folder"""
        user_name = event["source"]["user"]["username"]

        user = session.query("User where username is '{}'".format(user_name)).one()
        allowed_roles = ["Administrator", "Project Manager"]
        user_roles = [role["role"]["name"] for role in user["user_security_roles"]]
        if not any(role in allowed_roles for role in user_roles):
            return False

        return True

    def interface(self, session, entities, event):
        '''returns a UI with dropdown menu

        creates ftrack "["data"]["values"], which need to be fetched using .get()
        # '''

        project = entities[0]['project']

        data_all = []

        for user_role in project['user_security_role_projects']:
            user = user_role['user_security_role']['user']
            data = {}
            data['label'] = str(user['first_name'] + " " + user['last_name'])
            data['value'] = user['id']
            if user['id'] not in [d['value'] for d in data_all]:
                data_all.append(data)

        if not event['data'].get('values', {}):

            return [
        {
            "label": "Select User to Own Notes",
            "type": "enumerator",
            "name": "user_selection",
            "data": data_all,},

            {
            "label": "Select Type",
            "type": "enumerator",
            "name": "type_selection",
            "data": [
                {"label": "Assets", "value": "assets"},
                {"label": "Shots", "value": "shots"},
            ],

        },
        {
            "label":"Prefix:",
            "type": "textarea",
            "name":"prefix",
        },
        {
            "label": "Paste CSV Data",
            "type": "textarea",
            "name": "csv_input",

        },
        {
            "label":"Suffix:",
            "type": "textarea",
            "name":"suffix",
        },

    ]


    def launch(self, session, entities, event):


        project_name = entities[0]['project']['name']

        type_selection = event["data"]["values"].get("type_selection")
        prefix = event["data"]["values"].get("prefix")
        suffix = event["data"]["values"].get("suffix")
        if not type_selection:
            print("type selection is empty")
            return False
        else:
            print(type_selection)

        csv_data = event["data"]["values"].get("csv_input")
        if not csv_data:
            print("CSV input is empty.")
            return False
        else:
            print(csv_data)

        user = event["data"]["values"].get("user_selection")
        if not user:
            user = session.query("User where username is '{0}'".format(event["source"]["user"]["username"])).one()
        else:
            user = session.query("User where id is '{0}'".format(user)).one()

        self.parse_csv(csv_data, type_selection, prefix, suffix, project_name,user, event, session)

        return True

    def add_notes_to_ftrack(self, parent_name, notes, task_name, task_type, type_selection, prefix, suffix, project_name, user, event, session):
            """Function to process asset_name and notes."""

            if type_selection == "assets":
                task = session.query("Task where type.name is '{}' and parent.name is '{}' and project.name is '{}'".format(task_type, parent_name, project_name)).one()

            elif type_selection == "shots":
                print(parent_name, task_name)
                task = session.query("Task where name is '{}' and parent.name is '{}' and project.name is '{}'".format(task_name, parent_name, project_name)).one()

            lines = notes.split("\n")
            new_lines = []
            for line in lines:
                if line.startswith("- ") :
                    line = line.replace("- ", "&bull; ")
                line = line.replace("\t", "&#9;")
                new_lines.append(line)
            notes = "<br>".join(new_lines)


            if prefix:
                notes = prefix +"<br><br>"+ notes
            if suffix:
                notes = notes + "<br><br>" + suffix

            new_note = task.create_note(notes, user)

            print(task["name"] +" " +parent_name)
            print("notes: " +notes)
            print(f"Adding notes to FTrack: {parent_name} -> {notes}")
            return  {
                'success': True,
                'message': f"Adding notes to FTrack: {parent_name} -> {notes}"
                        }
            print("note with content already exist, skipping")


    def parse_csv(self,csv_data, type_selection, prefix, suffix, project_name, user, event, session):
        """Parses CSV text and processes each row."""
        reader = csv.DictReader(io.StringIO(csv_data), delimiter='\t')

        for row in reader:
            asset_name = row.get("asset_name", "").strip()
            shot_name = row.get("shot_name", "").strip()
            notes = row.get("notes", "").strip()
            task_name = row.get("task_name", "").strip()
            task_type = row.get("task_type", "").strip()
            if not task_type:
                task_type = task_name


            if type_selection == "assets":
                if asset_name and notes:
                    self.add_notes_to_ftrack(asset_name, notes, task_name, task_type, type_selection, prefix, suffix, user, project_name, event, session)
                    session.commit()


            elif type_selection == "shots":
                if shot_name and notes:
                    self.add_notes_to_ftrack(shot_name, notes, task_name, task_type, type_selection, prefix, suffix, project_name, user, event, session)
                    session.commit()



def register(session):
    '''Register plugin. Called when used as an plugin.'''
    addNotesFromCsv(session).register()



# if __name__ == '__main__':
#     logging.basicConfig(level=logging.INFO)
#     # Register and start listening for the action
#     register(session)
#     # Start event hub to keep the script running
#     session.event_hub.wait()
