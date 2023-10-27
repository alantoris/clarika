from typing import Any
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from nodes.models import Node


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
    
    def create_node(self, parent_id, value, children=None):
        data = dict(parent=parent_id, value=value)
        if children:
            data.update(children=children)
        response = self.client.post(
            f'/nodes/', 
            data,
            format="json"
        )
        return response
    
    def test_create_ok(self):
        response = self.create_node(self.root_node_pk, self.new_value)
        self.assertEquals(status.HTTP_201_CREATED, response.status_code)
        self.assertEquals(
            sorted([
                'id',
                'value',
                'parent'
            ]), sorted(response.data.keys()))
        
    def test_create_parent_not_exist(self):
        response = self.create_node(self.not_existing_node_id, self.new_value)
        self.assertEquals(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEquals(
            sorted([
                'parent'
            ]), sorted(response.data.keys()))
        
    def test_create_with_subtree_ok(self):
        response = self.create_node(self.root_node_pk, self.new_node_value, children=self.sub_tree)
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
    
    def test_delete_ok(self):
        response = self.create_node(self.root_node_pk, self.new_node_value)
        self.assertEquals(status.HTTP_201_CREATED, response.status_code)
        self.assertEquals(
            sorted([
                'id',
                'value',
                'parent'
            ]), sorted(response.data.keys()))
        new_node_id = response.data['id']
        response = self.client.delete(
            f'/nodes/{new_node_id}/', 
            format="json"
        )
        self.assertEquals(status.HTTP_204_NO_CONTENT, response.status_code)
        deleted_node = Node.objects.get(pk=new_node_id)
        self.assertEquals(deleted_node.deleted, True)

    def test_delete_not_found(self):
        response = self.client.delete(
            f'/nodes/{self.not_existing_node_id}/', 
            format="json"
        )
        self.assertEquals(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_delete_with_children_ok(self):
        response = self.create_node(self.root_node_pk, self.new_node_value)
        self.assertEquals(status.HTTP_201_CREATED, response.status_code)
        self.assertEquals(
            sorted([
                'id',
                'value',
                'parent'
            ]), sorted(response.data.keys()))
        
        new_node_id = response.data['id']
        response = self.create_node(new_node_id, self.new_node_value)
        self.assertEquals(status.HTTP_201_CREATED, response.status_code)
        self.assertEquals(
            sorted([
                'id',
                'value',
                'parent'
            ]), sorted(response.data.keys()))
        child_node_id = response.data['id']
        response = self.client.delete(
            f'/nodes/{new_node_id}/', 
            format="json"
        )
        self.assertEquals(status.HTTP_204_NO_CONTENT, response.status_code)

        deleted_node = Node.objects.get(pk=new_node_id)
        self.assertEquals(deleted_node.deleted, True)
        child_node = Node.objects.get(pk=child_node_id)
        self.assertEquals(child_node.deleted, True)

    def test_restore_deleted_node_ok(self):
        response = self.create_node(self.root_node_pk, self.new_node_value)
        self.assertEquals(status.HTTP_201_CREATED, response.status_code)
        self.assertEquals(
            sorted([
                'id',
                'value',
                'parent'
            ]), sorted(response.data.keys()))
        new_node_id = response.data['id']
        response = self.client.delete(
            f'/nodes/{new_node_id}/', 
            format="json"
        )
        self.assertEquals(status.HTTP_204_NO_CONTENT, response.status_code)
        deleted_node = Node.objects.get(pk=new_node_id)
        self.assertEquals(deleted_node.deleted, True)

        response = self.client.post(
            f'/nodes/{new_node_id}/restore/', 
            format="json"
        )
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(
            sorted([
                'id',
                'value',
                'parent'
            ]), sorted(response.data.keys()))

    def test_restore_node_with_parent_deleted_fail(self):
        response = self.create_node(self.root_node_pk, self.new_node_value)
        self.assertEquals(status.HTTP_201_CREATED, response.status_code)
        self.assertEquals(
            sorted([
                'id',
                'value',
                'parent'
            ]), sorted(response.data.keys()))
        
        new_node_id = response.data['id']
        response = self.create_node(new_node_id, self.new_node_value)
        self.assertEquals(status.HTTP_201_CREATED, response.status_code)
        self.assertEquals(
            sorted([
                'id',
                'value',
                'parent'
            ]), sorted(response.data.keys()))
        
        child_node_id = response.data['id']
        response = self.client.delete(
            f'/nodes/{new_node_id}/', 
            format="json"
        )
        self.assertEquals(status.HTTP_204_NO_CONTENT, response.status_code)

        deleted_node = Node.objects.get(pk=new_node_id)
        self.assertEquals(deleted_node.deleted, True)

        child_node = Node.objects.get(pk=child_node_id)
        self.assertEquals(child_node.deleted, True)

        response = self.client.post(
            f'/nodes/{child_node_id}/restore/', 
            format="json"
        )
        self.assertEquals(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEquals(
            sorted([
                'non_field_errors',
            ]), sorted(response.data.keys()))
