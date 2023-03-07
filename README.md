

##           FAST Maze API

####  Description:

A small app which handles user authentication with token.
You can create your own user then authenticate and create mazes.
After that you can solve them using either min or max paths. The min
will be the minimum path and max for the maximum path. Behind the scenes
there are BFS algorithms.

There are a few parts of the application:
- User creation
- Mazes creation
- Admin, user administration
- And a HTML section which is still in development.

The application works as follows.

1. From them OpenAPi (Swagger ) /docs url you create your onw user.
Here we use an RS264 algorithm to encode passwords, so the passwords will be hashed and
stored as hashes in database. The passwords will not be visible on plain text
2. You are free to create maze by following the rules. You may have some
wrong inputs but validations schemas are taking care of that your input will match
the application requirements
3. Solve maze will generate a maze solution. For the moment a DFS algorithm will generate
the longest path (almost because it is not guaranteed to be the longest). There
is in development the shortest path with a Dijkstra like algorithm

Still in development is the JavaScript part from the HTML section where the intention is
to show the mazes solutions.

Ahh. Almost forgot. The application is using the token authentication. So after you create
your user you must authenticate to create a user and be authorized. Not all the operations
are needing authentication. 