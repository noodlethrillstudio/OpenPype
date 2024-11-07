
from openpype_modules.ftrack.lib import BaseAction, statics_icon
from openpype.lib import Logger
class TransferNotes(BaseAction):

    label = 'Transfer notes'
    identifier = 'transfer.notes'
    description = 'Transfer notes from one task to another within a shot folder'
    icon = "ftrack", "action_icons", "SortReview.svg"


    def discover(self, session, entities, event):

        """Return True when entities contains a single Task Object"""
        ''' Validation '''
        valid = True

        # Check for multiple selection.
        if len(entities) > 1:
            valid = False
        # Check for valid entities.
        valid_entity_types = ['task']
        for entity in entities:
            if entity.entity_type.lower() not in valid_entity_types:
                valid = False
                break

        return valid



    def interface(self, session, entities, event):
        '''returns a UI with dropdown menu

        creates ftrack "["data"]["values"], which need to be fetched using .get()
        # '''
        self.log.info('{0}'.format(entities[0]['id']))

        if not event['data'].get('values', {}):

            try:

                task_id = entities[0]['id']
                task = self.session.query('Task where id is "{0}"'.format(task_id)).one()
                self.log.info(f'interface task query succesful: {task}')
            except Exception as e:
                self.log.error(f'Error during interface task session query: {e}')


            try:
                other_tasks = self.get_other_tasks(task)
                self.log.info('other task get successful')
            except Exception as e:
                self.log.error(f'Error during get_other_tasks interface: {e}')

            task_names = []
            for task in other_tasks:
                task_names.append(task['name'])


            data_all = []
            for other_task in other_tasks:
                data = {}
                data['label'] = '{0}'.format(other_task['name'])
                data['value'] = '{0}'.format(other_task['id'])

                data_all.append(data)


            return [
                {
                    'type': 'label',
                    'value': 'Choose a task to transfer notes to'
                },

                {
                    'type': 'boolean',
                    'label':'Un-Completed notes only',
                    'name':'checkbox',
                    'value':True
                },

                {
                    'type':'enumerator',
                    'name':'destination_task',
                    'data': data_all
                }

                ]
        return

    def launch(self, session, entities, event):
            '''Callback method for the custom action.

            '''
            if 'values' not in event['data']:
                return

            entity_id = entities[0]['id']
            values = event['data'].get('values',{})
            task = self.session.query('Task where id is "{0}"'.format(entity_id)).one()
            task_id = task['id']

            notes = self.get_notes(task_id, values)

            des_task = self.session.query('Task where id is {0}'.format(values['destination_task'])).one()

            self.transfer_notes( notes, des_task)

            session.commit()


            return  {
            'success': True,
            'message': 'Transferred notes from {0} to {1} succesfully'.format(task['name'], des_task['name'])
                    }


    def get_other_tasks(self, task):

        other_tasks = self.session.query(
            'Task where parent_id is "{0}" and''(id != "{1}")'.format(task['parent_id'],task['id'])
             )

        return other_tasks



    def get_notes(self, task_id, values):
        """Returns an array of all the notes attached to the chosen task"""
        uncompleted_only = values['checkbox']
        versions = self.session.query('AssetVersion where task.id is "{0}"'.format(task_id))

        notes_to_add = []

        if uncompleted_only == True:
            task_notes = self.session.query('Note where parent_id is "{0}" and completed_at is None'.format(task_id)).all()
        elif uncompleted_only == False:
            task_notes = self.session.query('Note where parent_id is "{0}"'.format(task_id)).all()

        for task_note in task_notes:
            notes_to_add.append(task_note)


        for version in versions:
            if uncompleted_only == True:
                notes = self.session.query('Note where parent_id is "{0}" and completed_at is None '.format(version['id'])).all()
                for note in notes:
                    notes_to_add.append(note)
            elif uncompleted_only == False:
                notes = self.session.query('Note where parent_id is "{0}"'.format(version['id'])).all()
                for note in notes:
                    notes_to_add.append(note)

        return notes_to_add


    def transfer_notes(self, notes, des_task ):

        for note in notes:
            # print(note['content'])
            # print(note['in_reply_to'])
            # print(note['in_reply_to_id'])
            # for reply in note['replies']:
            #     print(reply['content'])
            # for link in note['note_label_links']:
            #     print(link)
            # print("next note : ")

            if note['in_reply_to'] == None:
                new_note = self.session.create('Note',{

                    'content': note['content'],
                    'date': note['date'],
                    'thread_activity': note['thread_activity'],
                    'user_id': note['user_id'],
                #     # 'in_reply_to_id': note['in_reply_to_id'],
                    #'category_id': note['category_id'],
                    'is_todo': note['is_todo'],
                    'completed_by_id': note['completed_by_id'],
                    'completed_at' : note['completed_at'],
                    'completed_by' : note['completed_by'],
                    'author' : note['author'],
                  # 'metadata' : note ['metadata'],
                    #'replies' : note ['replies'],
                    #if has replies, get those replies
                    'category' : note['category'],
                    'in_reply_to' : note['in_reply_to'],
                    #if in_reply_to != None, do something
                    'note_components' : note['note_components'],
                #     # 'note_label_links': note['note_label_links'],
                    'recipients' : note['recipients'],
                    'frame_number' : note['frame_number']
                })

                des_task['notes'].append(new_note)

                if note['replies'] != None:
                    replies = note['replies']
                    for reply in replies:
                        new_reply = self.session.create('Note',{
                            'content': reply['content'],
                            'date': reply['date'],
                            'user_id': reply['user_id'],'is_todo': note['is_todo'],
                            'completed_by_id': reply['completed_by_id'],
                            'completed_at' : reply['completed_at'],
                            'completed_by' : reply['completed_by'],
                            'author' : reply['author'],
                            'in_reply_to' : new_note,
                            'in_reply_to_id' : new_note['id'],
                            'note_components' : reply['note_components'],
                            'recipients' : reply['recipients'],
                            'frame_number' : reply['frame_number'],
                            'parent_id': new_note['id'],
                            'is_todo': reply['is_todo'],
                        })
                        des_task['notes'].append(new_reply)

        return



def register(session):
    '''Register plugin. Called when used as an plugin.'''
    TransferNotes(session).register()
