from ariadne import graphql_sync, make_executable_schema, ObjectType, QueryType, MutationType
from ariadne.explorer import ExplorerGraphiQL
from flask import Flask, jsonify, request, current_app
from flask_sqlalchemy import SQLAlchemy
import logging
logging.basicConfig(level=logging.DEBUG)  # Enable debug logging


app = Flask(__name__)

try:
    # Attempt to set the database URI
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///posts.db"
    db = SQLAlchemy(app)
except Exception as e:
    print(f"Error configuring database: {e}")
    exit(1)


type_defs = """
    type Post {
        id: ID
        title: String
        body: String
    }

    type Query {
        hello: String!
        posts(offset: Int, limit: Int): [Post!]!  # List of non-nullable posts
    }

    type Mutation {
        createPost(title: String!, body: String!): Post!
    }

"""

query = QueryType()
mutation = MutationType()

@query.field("hello")
def resolve_posts(obj, info):
    return "Hi"

@query.field("posts")
def resolve_posts(obj, info, offset=0, limit=10):
    # return Post.query.all()  # Fetch all posts
    return Post.query.offset(offset).limit(limit)  # Fetch a chunk of posts

@mutation.field("createPost")
def resolve_create_post(obj, info, title, body):
    if not title or not body:
        raise Exception("Please provide title and body for the post.")

    new_post = Post(title=title, body=body)
    try:
        db.session.add(new_post)
        db.session.commit()
    except Exception as e:
        raise Exception("Exception caused " + str(e))
    return new_post

schema = make_executable_schema(type_defs, [query, mutation])

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(80))
    body = db.Column(db.Text)
    
with app.app_context():
    db.create_all()  # This will create the table if it doesn't exist

# Retrieve HTML for the GraphiQL.
# If explorer implements logic dependant on current request,
# change the html(None) call to the html(request)
# and move this line to the graphql_explorer function.
explorer_html = ExplorerGraphiQL().html(None)


@app.route("/graphql", methods=["GET"])
def graphql_explorer():
    # On GET request serve the GraphQL explorer.
    # You don't have to provide the explorer if you don't want to
    # but keep on mind this will not prohibit clients from
    # exploring your API using desktop GraphQL explorer app.
    return explorer_html, 200


@app.route("/graphql", methods=["POST"])
def graphql_server():
    # GraphQL queries are always sent as POST
    data = request.get_json()

    # Note: Passing the request to the context is optional.
    # In Flask, the current request is always accessible as flask.request
    success, result = graphql_sync(
        schema,
        data,
        context_value={"request": request},
        debug=app.debug
    )

    status_code = 200 if success else 400
    return jsonify(result), status_code


if __name__ == "__main__":
    app.run(debug=True)


    