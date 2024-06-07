# exploring-graphql
 
Install necessary packages:
pip3 install Flask ariadne Flask-SQLAlchemy

Run application using 
python app.py

Access app locally via http://127.0.0.1:5000/graphql

Try a test request on graphql UI:
{
  posts {
    id
  }
}

## TYPES

### Scalar Types
Basic non-divisible types
1. `STRING`
2. `INT`
3. `BOOLEAN`
4. `FLOAT`
5. `ID`

### Object Types
Custom types that contains one or more scalar types and/or objects
```
type User {
    id: ID!
    username: STRING!
    email: STRING!
    posts: [Post!]! #List of non-nullable posts
}
```

### Enum Types
These are pre-defined string values that is useful for representing categorical fields
```
enum PostStatus {
    CREATED
    EDITED
    DELETED
}
```

### Input Types
Used for defining arguments passed into mutations and fields.

```
type Mutation {
    createPost(data: CreatePostInput!): Post!
}

input CreatePostInput {
    title: STRING!
    body: STRING
    published: BOOLEAN
}

```

## OPERATIONS
Actions clients can use to interact with data

### Queries
Retrieves data from a data store. You can define more than one query under the same Query type.
```
type Query {
  posts(title: String): [Post!]!  # Optional title filter
  user(username: String) : User!
}
```

### Mutations
Add new or modifying/deleting existing data

### Subscriptions (less commonly used)
Receive real time updates from server on data that you are subscribed to


