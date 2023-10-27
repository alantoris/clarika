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
            value: "NAME"   // Node name
            parent: 1       // Node parent id
        }
    - response
        {
            value: "NAME"   // Node name
            parent: 1       // Node parent id
        }
