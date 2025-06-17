import io
import csv
import logging
from openpype_modules.ftrack.lib import BaseAction, statics_icon
import ftrack_api


RUN_AS_ACTION = True  # Set to False to run as an event listener.
UPDATE_LABELS = False  # Set to False to create comments instead.


class createAnimationListReview(BaseAction):
    label = 'Create Animation Review'
    identifier = 'com.ftrack.recipes.create_animation_review'
    description = 'Create new list for animation review. Add animation shots if they exist, blocking shots if not, and animatic shots if blocking doesn\'t exist.'

    def discover(self, session, entities, event):
        if entities[0].entity_type  != 'Episode' or len(entities) != 1:
            return False
        return True

    def interface(self, session, entities, event):
        '''returns a UI with dropdown menu

        creates ftrack "["data"]["values"], which need to be fetched using .get()
        # '''
        if not event['data'].get('values', {}):
            return [
                    {
                        'type': 'enumerator',
                        'name': 'category',
                        'label': 'Blocking or Animation?:',
                        'data': [
                            {
                                'value': 'Blocking',
                                'label': 'Blocking',
                            },
                            {
                                'value': 'Animation',
                                'label': 'Animation',
                            },
                        ]
                    },

                    {
                        'type': 'text',
                        'label':'Review List Name',
                        'name':'review_list_name',
                        'value':'...'
                    },
                    ]
        return



    def launch(self, session, entities, event):
        episode = entities[0]
        episode_id = episode["id"]
        sequence = session.query(f"Sequence where parent_id is {episode_id}").one()
        shots = session.query(f"Shot where parent_id is {sequence['id']}").all()

        print(f"Episode: {episode['name']}")
        print(f"Shots: {len(shots)}")

        if event['data'].get('values', {}).get('category') == 'Blocking':
            category = session.query(
                f"ListCategory where name is 'Series Director - Blocking Review'").one()

        elif event['data'].get('values', {}).get('category') == 'Animation':
            category = session.query(
                f"ListCategory where name is 'Series Director - Animation Review'").one()

        items_for_review = []
        review_list_name = event['data'].get('values', {}).get('review_list_name')
        version_list = session.create("AssetVersionList", {
        "name": f"{review_list_name}",
        "category_id": category["id"],
        "is_open": True,
        "project_id": episode["project_id"],
        })

        session.commit()

        for shot in shots:
            print(f"Shot: {shot['name']}")

            animation_task = session.query(f"Task where parent_id is {shot['id']} and type.name is Animation").one()
            animation_task_version = get_task_version(session, animation_task, shot)
            if animation_task_version:
                items_for_review.append(animation_task_version)
                continue

            blocking_task = session.query(f"Task where parent_id is {shot['id']} and type.name is Blocking").one()
            blocking_task_version = get_task_version(session, blocking_task, shot)
            if blocking_task_version:
                items_for_review.append(blocking_task_version)
                continue

            animatic_version = get_shot_version(session, shot)
            if animatic_version:
                items_for_review.append(animatic_version)
                continue


        version_list["items"].extend(items_for_review)
        session.commit()

        return True

def get_task_version(session, task, shot):

    task_version = has_versions(session, task)

    if task_version != False:
        return task_version

    else:
        return False

def get_shot_version(session, shot):
    shot_version = has_shot_versions(session, shot)
    if shot_version != False:
        print(f"Animatic task found for {shot['name']}")
        return shot_version
    else:
        return False


def has_versions(session, task):
    '''Check if task has versions. If it does, return True. If not, return False.'''
    versions = session.query(
        f"AssetVersion where task_id is {task['id']}").all()
    if len(versions) > 0:
        for version in versions:
            if version["is_latest_version"]:
                return version

    else:
        return False

def has_shot_versions(session, shot):
    '''Check if shot has versions. If it does, return True. If not, return False.'''
    print("has shot versions started")
    assets = shot["assets"]
    for asset in assets:
        if asset["name"] == "reviewReference":
            versions = session.query(f"AssetVersion where asset_id is {asset['id']}").all()

            if len(versions) > 0:
                for version in versions:
                    print(f"Shot version found: {asset['name']}, {str(version['version'])}")
                    if version["is_latest_version"]:
                        return version
            else:
                return False
    print("No shot versions found")
    return False

def register(session):
    '''Register plugin. Called when used as an plugin.'''
    createAnimationListReview(session).register()
