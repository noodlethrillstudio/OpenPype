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

        valid = True

        # # Check for multiple selection.
        # if len(entities) != 1:
        #     valid = False
        # if entities[0]["type"] != "Folder":
        #     valid = False

        return valid

    def interface(self, session, entities, event):
        '''returns a UI with dropdown menu

        creates ftrack "["data"]["values"], which need to be fetched using .get()
        # '''


        if not event['data'].get('values', {}):

            return [
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
            "label": "Paste CSV Data",
            "type": "textarea",
            "name": "csv_input",

        },
    ]


    def launch(self, session, entities, event):

        type_selection = event["data"]["values"].get("type_selection")
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

        self.parse_csv(csv_data, type_selection, event, session)


        return True

    def add_notes_to_ftrack(self, parent_name, notes, task_name, task_type, type_selection, user, event, session):
            """Function to process asset_name and notes."""
            if type_selection == "assets":
                task = session.query("Task where type.name is '{}' and parent.name is '{}'".format(task_type, parent_name)).one()

            elif type_selection == "shots":
                print(parent_name, task_name)
                task = session.query("Task where name is '{}' and parent.name is '{}'".format(task_name, parent_name)).one()
            notes = "BRIEF NOTES: " + notes

            if not task["notes"]:
                new_note = session.create("Note", {
                "content": notes,
                "author" : user
                })

                task["notes"] = [new_note]
                session.commit()
                print(task["name"] +" " +parent_name)
                print("notes: " +notes)
                print(f"Adding notes to FTrack: {parent_name} -> {notes}")
                return  {
                    'success': True,
                    'message': f"Adding notes to FTrack: {parent_name} -> {notes}"
                            }
            print("note with content already exist, skipping")


    def parse_csv(self,csv_data, type_selection, event, session):
        """Parses CSV text and processes each row."""
        reader = csv.DictReader(io.StringIO(csv_data), delimiter='\t')
        user = session.query("User where username is '{0}'".format(event["source"]["user"]["username"])).one()
        for row in reader:
            asset_name = row.get("asset_name", "").strip()
            shot_name = row.get("shot_name", "").strip()
            notes = row.get("notes", "").strip()
            task_name = row.get("task_name", "").strip()
            task_type = row.get("task_type", "").strip()


            if type_selection == "assets":
                if asset_name and notes:
                    self.add_notes_to_ftrack(asset_name, notes, task_name, task_type, type_selection, user, event, session)

            elif type_selection == "shots":
                if shot_name and notes:
                    self.add_notes_to_ftrack(shot_name, notes, task_name, task_type, type_selection, user, event, session)


def register(session):
    '''Register plugin. Called when used as an plugin.'''
    addNotesFromCsv(session).register()



# if __name__ == '__main__':
#     logging.basicConfig(level=logging.INFO)
#     # Register and start listening for the action
#     register(session)
#     # Start event hub to keep the script running
#     session.event_hub.wait()
