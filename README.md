# Pyckish
### AWS Lambda Event extractor/parser/validator" 
Pyckish is an "extract, parse and validate" solution to allow ease of use when dealing with AWS Lambdas. It aims
to make using Lambdas to handle HTTP requests an alternative that works similarly to other frameworks for back-end
applications, like FastAPI.

Currently, it can be used to extract HTTP data that comes in the event dictionary. It extracts from the dictionary,
parses it and validates it. It relies heavily on Pydantic, and will make your life simpler if you only like to deal with validated and
correctly typed data.

#### Instead of doing this:
```python
def lambda_handler(event: dict, context: dict) -> float:
    auth = event['headers']['authorization_token']
    store = event['pathParameters']['store']
    item = event['body']
    
    user = get_user(auth)
    price = get_price(item, store, user)
    return price
```

#### Do this:
```python
import pyckish
from pyckish.http_elements import Body, Header, PathParameter
from my_models import Item

@pyckish.AWSEventExtractor()
def lambda_handler(
        auth: str = Header(alias='authorization_token'),
        store: str = PathParameter(default='my_store'),
        item: Item = Body()
) -> float:
    user = get_user(auth)
    price = get_price(item.dict(), store, user)
    return price
```

And get validation and parsing free of trouble thanks to integration with Pydantic. Enjoy the advantages of a much
more robust codebase, leaving behind having to extract and manage issues related to missing/wrong values.


# Motivation

Today, together with AWS API Gateway, it is possible to use only AWS Lambdas as back-end for your application.
The problem is, unlike modern Frameworks, like FastAPI and Starlite, using only AWS Lambdas requires you to develop
your own solutions for extracting, parsing, validating as well as creating error handling for the inputs of your code.
There are solutions that allow you to use ASGI Frameworks with AWS Lambdas, like Mangum. But it is yet another 
technology that sits above your bulky framework. Personally, I think that the problem could be solved in a more 
simple and direct manner. Pyckish aims to be that solution.

Using tools like Serverless Framework with its integration with CloudFormation, many AWS Lambdas can be deployed
from a single repository. Those "monorepos" solutions could also make heavy use of Pyckish in order to handle its
inputs.

Right now, Pyckish is a tiny baby, and I'm not sure of its future. Weather it will become a full Framework with more
capabilities than Chalice, or it is going to remain as a simple "extractor/parser/validator" I do not know.

But I encourage you to try, simplicity and types will seduce you into it.