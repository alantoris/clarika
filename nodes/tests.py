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
        self.not_existing_node_id = 100
        self.new_node_value = "VALUE"
        self.new_value = "NEW_VALUE"
        self.sub_tree = [
            {
                "value": self.new_node_value,
                "children": [
                    {
                        "value": self.new_node_value,
                        "children": []
                    }
                ]
            }
        ]
    
    def test_create_ok(self):
        response = self.client.post(
            f'/nodes/', 
            dict(parent=self.root_node_pk, value=self.new_node_value),
            format="json"
        )
        self.assertEquals(status.HTTP_201_CREATED, response.status_code)
        self.assertEquals(
            sorted([
                'id',
                'value',
                'parent'
            ]), sorted(response.data.keys()))
        
    def test_create_parent_not_exist(self):
        response = self.client.post(
            f'/nodes/', 
            dict(parent=self.not_existing_node_id, value=self.new_node_value),
            format="json"
        )
        self.assertEquals(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEquals(
            sorted([
                'parent'
            ]), sorted(response.data.keys()))
        
    def test_create_with_subtree_ok(self):
        response = self.client.post(
            f'/nodes/', 
            dict(parent=self.root_node_pk, value=self.new_node_value, children=self.sub_tree),
            format="json"
        )
        self.assertEquals(status.HTTP_201_CREATED, response.status_code)
        self.assertEquals(
            sorted([
                'id',
                'value',
                'parent'
            ]), sorted(response.data.keys()))

    def test_edit_node_value_ok(self):
        response = self.client.patch(
            f'/nodes/{self.root_node_pk}/', 
            dict(value=self.new_value),
            format="json"
        )
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(
            sorted([
                'id',
                'value',
                'parent'
            ]), sorted(response.data.keys()))

    def test_edit_node_value_not_found(self):
        response = self.client.patch(
            f'/nodes/{self.not_existing_node_id}/', 
            dict(value=self.new_value),
            format="json"
        )
        self.assertEquals(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertEquals(
            sorted([
                'detail'
            ]), sorted(response.data.keys()))
