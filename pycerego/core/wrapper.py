import pprint
from pycerego.core.auth import CeregoMisc
from pycerego.core.endpoint import _get_profile, _get_set, _get_series_index, _create_set, _create_set_concept, \
    _create_set_item, _create_set_facet, _get_items_in_set

__author__ = 'jacob'

class CeregoWrapper(object):
    
    def __init__(self):
        
        self.misc = 0
        self.data_history_queue = []
        self.loaded_set_data = {}
    
    def set_misc(self, token, host="http://api.cerego.com/v2/"):
        
        self.misc = CeregoMisc(token, host)

    def get_profile(self):

        response = _get_profile(self.misc)
        self.data_history_queue.append(response)
        return response

    def get_set(self, set_id):

        response = _get_set(self.misc, set_id)
        self.data_history_queue.append(response)
        return response

    def get_items_in_set(self, set_id):

        response = _get_items_in_set(self.misc, set_id)
        self.data_history_queue.append(response)
        return response

    def load_set_data(self, set_id):

        self.loaded_set_data['id'] = set_id
        self.loaded_set_data['head'] = self.get_set(set_id)
        item_data = self.get_items_in_set(set_id)
        item_names = []
        for item in item_data:
            item_names.append(item['association_collection']['concept']['text'])
        self.loaded_set_data['items'] = item_names
        return self.loaded_set_data

    def get_series_index(self):

        response = _get_series_index(self.misc)
        self.data_history_queue.append(response)
        return response

    def create_set(self, name, lang="English"):

        response = _create_set(self.misc, name, lang)
        self.data_history_queue.append(response)
        return response

    def create_set_concept(self, set_id, params):

        response = _create_set_concept(self.misc, set_id, params)
        self.data_history_queue.append(response)
        return response

    def create_set_item(self, set_id, concept_id):
        
        response = _create_set_item(self.misc, set_id, concept_id)
        self.data_history_queue.append(response)
        return response

    def create_set_facet(self, item_id, set_id, association_concept_id):
        response = _create_set_facet(self.misc, item_id, set_id, association_concept_id)
        self.data_history_queue.append(response)
        return response

    def create_item_anchor_association(self, set_id, anchor, association):

        anchor_object = {"text": anchor}
        association_object = {"text": association}
        self.create_set_concept(set_id, anchor_object)
        self.create_set_concept(set_id, association_object)
        self.create_set_item(set_id, self.get_scope_id(is_concept=True, prev_state=1))
        return self.create_set_facet(self.get_scope_id(), set_id, self.get_scope_id(is_concept=True, prev_state=1))

    def get_scope_id(self, is_concept=False, prev_state=0):

        prev_response = self.data_history_queue[-(1 + prev_state)]
        if is_concept:
            return prev_response['concept']['id']
        else:
            return prev_response['id']

if __name__ == "__main__":

    token = "HSJXbAXVEcORLfp4bzyH9+mJqedIFgVXrMeJyDY0I5cV+x/M1B4NKKrXIKYKsdp1"
    cg_wrapper = CeregoWrapper()
    cg_wrapper.set_misc(token)
    pprint.pprint(cg_wrapper.load_set_data("735960"))
