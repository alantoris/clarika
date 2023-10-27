from typing import Any
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class NodesViewSetTest(TestCase):
    """
    Class to test list filtered and creation of Elements
    """
    def setUp(self):
        self.client = APIClient()
        self.root_node_pk = 1
        self.not_existing_parent_node_id = 100
        self.new_node_value = "VALUE"
    
    def test_create_ok(self):
        response = self.client.post(
            f'/nodes/', 
            dict(parent=self.root_node_pk, value=self.new_node_value),
            format="json"
        )
        self.assertEquals(status.HTTP_201_CREATED, response.status_code)
        self.assertEquals(
            sorted([
                'value',
                'parent'
            ]), sorted(response.data.keys()))
        
    def test_create_parent_not_exist(self):
        response = self.client.post(
            f'/nodes/', 
            dict(parent=self.not_existing_parent_node_id, value=self.new_node_value),
            format="json"
        )
        self.assertEquals(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEquals(
            sorted([
                'parent'
            ]), sorted(response.data.keys()))
