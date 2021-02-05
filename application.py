import uvicorn
from ariadne import QueryType, gql, make_executable_schema
from ariadne.asgi import GraphQL
from starlette.middleware.cors import CORSMiddleware

type_defs = gql("""
    type Query {
        hello: String!
    }
""")

query = QueryType()


@query.field("hello")
def resolve_hello(_, info):
    request = info.context["request"]
    user_agent = request.headers.get("user-agent", "guest")
    return "Hello, %s!" % user_agent


schema = make_executable_schema(type_defs, query)

application = app = CORSMiddleware(GraphQL(schema, debug=True),
                                   allow_origins=['*'], allow_methods="GET, POST")

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=5000)
