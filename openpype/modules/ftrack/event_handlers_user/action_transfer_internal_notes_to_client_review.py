import io
import csv
import logging
from openpype_modules.ftrack.lib import BaseAction, statics_icon
import ftrack_api
import json
import base64
import zlib

RUN_AS_ACTION = True  # Set to False to run as an event listener.
UPDATE_LABELS = False  # Set to False to create comments instead.


class transferInternalNotesToClientReview(BaseAction):
    label = 'Transfer Notes to Review'
    identifier = 'com.ftrack.recipes.transfer_notes_to_review'
    description = 'Transfer internal notes from version to client review.'

    def discover(self, session, entities, event):
        ''' Validation '''
        if (len(entities) != 1 or entities[0].entity_type != 'ReviewSession'):
            return False
        return True


    def launch(self, session, entities, event):
        ftrack_server = session.query("Location where name is 'ftrack.server'").one()

        review_session = entities[0]

        objects = review_session["review_session_objects"]

        for object in objects:
            version = object["asset_version"]


            for note in version["notes"]:
                new_note = self.copy_version_notes(session, note, object, ftrack_server)
        return True

    def is_valid_json(self, data):
        try:
            if isinstance(data, str):
                json.loads(data)
            elif isinstance(data, dict):
                json.dumps(data)  # Make sure it's serializable
            else:
                return False
            return True
        except (ValueError, TypeError):
            return False

    def decode_annotation_data(self, data):
        if isinstance(data, dict):
            return data
        if isinstance(data, str):
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                pass

            try:
                decoded_bytes = base64.b64decode(data)
                decompressed = zlib.decompress(decoded_bytes).decode('utf-8')


                clean_decompressed = self.remove_ids(json.loads(decompressed))


                return json.dumps(clean_decompressed)
            except Exception:
                return None
        return None

    def remove_ids(self, data):
        if isinstance(data, dict):
            data.pop("id", None)
            for key in data:
                data[key] = self.remove_ids(data[key])
        elif isinstance(data, list):
            data = [self.remove_ids(item) for item in data]
        return data

    def copy_note_component(self, session, new_note, note, old_note_component, object, ftrack_server):

        old_component = old_note_component["component"]

        resource_id = ftrack_server.get_resource_identifier(old_component)
        new_component = session.create('FileComponent', {
            'name': old_component["name"],
            'resource_identifier': resource_id,
            'file_type': old_component['file_type'],
            'project_id':old_component['project_id'],
            'size': old_component['size'],
            'system_type': old_component['system_type']
            })

        new_component_location = session.create('ComponentLocation',{
            'component': new_component,
            'resource_identifier':resource_id,
            'location': ftrack_server

        })
        session.create("NoteComponent", {
            "component_id": new_component["id"],
            "note_id": new_note["id"],
        })

        for key in old_component["metadata"]:
            new_component['metadata'][f'{key}'] = old_component["metadata"][f'{key}']

        if not old_component.get('metadata', {}).get('annotationData'):
            return

        data = old_component['metadata']['annotationData']

        if not self.is_valid_json(data):
            decoded_data = self.decode_annotation_data(data)
            if self.is_valid_json(decoded_data):
                session.create("ReviewSessionObjectAnnotation", {
                    'data': decoded_data,
                    'frame_number': note['frame_number'],
                    'review_session_object': object,
                })
                return

        if self.is_valid_json(data):
            session.create("ReviewSessionObjectAnnotation", {
                'data': data,
                'frame_number': note['frame_number'],
                'review_session_object': object,
            })
        return

    def copy_version_notes(self, session, note, object, ftrack_server ):
        if note['in_reply_to'] == None:
            new_note = session.create("Note",{
            'content': note['content'],
            'date': note['date'],
            'thread_activity': note['thread_activity'],
            'user_id': note['user_id'],
            'project_id': note['project_id'],
            'completed_by_id': note['completed_by_id'],
            'completed_at' : note['completed_at'],
            'completed_by' : note['completed_by'],
            'author' : note['author'],
            'category' : note['category'],
            'is_todo' : note['is_todo'],
            'recipients' : note['recipients'],
            'frame_number' : note['frame_number'],
            'parent_id': object['id'],
                })
            for key in note['metadata']:
                new_note['metadata'][f'{key}'] = note['metadata'][f'{key}']
            object["notes"].append(new_note)

            for note_component in note['note_components']:
                self.copy_note_component(session, new_note, note, note_component, object, ftrack_server)

            if note["replies"] != None:
                for reply in note["replies"]:
                    new_reply = session.create("Note",{
                        'content': reply['content'],
                        'date': reply['date'],
                        'thread_activity': reply['thread_activity'],
                        'user_id': reply['user_id'],
                        'project_id': reply['project_id'],
                        'completed_by_id': reply['completed_by_id'],
                        'completed_at' : reply['completed_at'],
                        'completed_by' : reply['completed_by'],
                        'author' : reply['author'],
                        'category' : reply['category'],
                        'is_todo' : reply['is_todo'],
                        'recipients' : reply['recipients'],
                        'frame_number' : reply['frame_number'],
                        'in_reply_to_id' : new_note['id'],
                        'parent_id': new_note['parent_id'],
                            })
                    for key in reply['metadata']:
                        new_reply['metadata'][f'{key}'] = reply['metadata'][f'{key}']
                    object["notes"].append(new_reply)

                    for note_component in reply['note_components']:

                        self.copy_note_component(session, new_reply, reply, note_component, object, ftrack_server)
        session.commit()
        return

# def register(session):
#     '''Register plugin. Called when used as an plugin.'''
#     transferInternalNotesToClientReview(session).register()
