# Clarika
Solution for python test of the Clarika selection process

## Instructions 

To execute this test it is enough to simply build the docker images generated using the docker compose file

`docker-compose build`

After its completion we will simply launch the django backend 

`docker-compose up`

After these steps we will have the backend available in our local environment on port 8000


## Considerations

- The application is inizializated with a root nood in the database (id = 1)

- The node model allows having nulls in the parent field since the root node will have this value, but a counter validation was added in the serializer since the other nodes that will be added to the tree should not have null parent


## Endpoints

 - Add new node
    - POST /nodes/
    - body 
        {
            value: "VALUE"   // Node value
            parent: 1       // Node parent id
        }
    - response
        {
            id: 2           // New node id
            value: "VALUE"   // Node value
            parent: 1       // Node parent id
        }


- Add new subtree to a node
    - POST /nodes/
    - body
        {
            "value": "VALUE",    // Node value
            "parent": 1,        // Node parent id
            "children": [       // SUB TREE
                {
                    "value": "SUB NODE VALUE", 
                    "children": [
                        {
                            "value": "SUB NODE 2 VALUE", 
                            "children": []
                        }
                    ]
                }
            ]
        }
    - response
        {
            id: 2           // New node id
            value: "VALUE"   // Node value
            parent: 1       // Node parent id
        }

- Set the value of a particular node
    - PATCH /nodes/<ID_NODE>/
    - body
        {
            "value": "NEW VALUE"
        }
    - response
        {
            id: 2               // Node id
            value: "NEW VALUE"  // Node new value
            parent: 1           // Node parent id
        }

- Delete a node
    - DELETE /nodes/<ID_NODE>/
    - body 
        {}
    - response
        {}

- Restore a node 
    - POST /nodes/<ID_NODE>/restore/
    - body 
        {}
    - response
        {
            id: 2               // Node id
            value: "VALUE"      // Node value
            parent: 1           // Node parent id
        }

- Restore a node, and restore also his children
    - POST /nodes/<ID_NODE>/restore/?children=true
    - body 
        {}
    - response
        {
            id: 2               // Node id
            value: "VALUE"      // Node value
            parent: 1           // Node parent id
        }

