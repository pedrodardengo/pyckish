<p align="center">
  <img alt="Midjourney attempt on pyckish logo" src="https://i.imgur.com/kqtYQTv.png" height="400">
</p>

# Pyckish

### -- Create _AWS Lambdas_ professionally with this micro framwork


[![PyPI](https://img.shields.io/pypi/v/pyckish)](https://pypi.org/project/pyckish/)

```bash
pip install pyckish
```


Pyckish is an "extract, parse and validate" solution to allow ease of use when dealing with _AWS Lambdas_, it also
allows creation of exception handlers to deal with exceptions. It aims to make using Lambdas to handle HTTP requests 
an alternative that works similarly to other frameworks for back-end applications, like FastAPI.

Currently, it can be used to extract HTTP data that comes in the event/context dictionary. It extracts from 
the dictionary, parses it and validates it. It relies heavily on Pydantic, and will make your life simpler if you 
only like to deal with validated and correctly typed data.

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


@pyckish.Lambda()
def lambda_handler(
        auth: str = Header(alias='authorization_token'),
        store: str = PathParameter(),
        item: Item = Body()
) -> float:
    user = get_user(auth)
    price = get_price(item, store, user)
    return price
```

And get validation and parsing free of trouble thanks to integration with Pydantic. Enjoy the advantages of a much
more robust codebase, leaving behind having to extract and manage issues related to missing/wrong values.

## What are _AWS Lambda Functions_
Lambdas are just simple functions that you can write in languages like Python, Javascript, etc. that are meant to be 
deployed on AWS. They can be activated/triggered by AWS whenever an event happens, it might a client application 
hitting on AWS API Gateway or a cron-job activation triggered by AWS Event Bridge. AWS manages every computer resource
for you, this makes AWS exceptionally easy to deploy. It is integrated with most things on AWS, meaning there is almost
always a way to do what you want with Lambdas.

The interesting thing about Lambdas is that beyond being just a simple functions easy to write that you can extract data
from its inputs and put whenever logic you want inside it, Lambdas also are really, really cheap. You could activate it 
a million times per month with being charged, and this is only on AWS free tier. All of this makes Lambdas an 
attractive technology for most companies.

Lambdas, normally have only two parameters, both are two JSON's that are converted to python dictionaries, event and 
context. This library extracts, validates and parses values from those parameters.

## Motivation

(Today, together with AWS API Gateway, it is possible to use only AWS Lambdas as back-end for your application.
The problem is, unlike modern Frameworks, like FastAPI and Starlite, using only AWS Lambdas requires you to develop
your own solutions for extracting, parsing, validating as well as creating error handling for the inputs of your code.
There are solutions that allow you to use ASGI Frameworks with AWS Lambdas, like Mangum. But it is yet another 
technology that sits above your bulky framework. Personally, I think that the problem could be solved in a more 
simple and direct manner. Pyckish aims to be that solution.

Using tools like Serverless Framework with its integration with CloudFormation, many AWS Lambdas can be deployed
from a single repository. Those "monorepos" solutions could also make heavy use of Pyckish in order to handle its
inputs.

Right now, Pyckish is a tiny baby, and I'm not sure of its future. Weather it will become a full Framework with more
capabilities than Chalice Framework, or it is going to remain as a simple "extractor/parser/validator" I do not know.

But I encourage you to try, simplicity and types will seduce you into it.

## Usage

Currently, Pyckish provides you with these features:

- Extract/parse/validate the data contained in the Lambda Inputs all with adequate Exceptions raised in case of
failure.
- Improves readability of your Lambda function by clearly stating the data your Lambda function requires.
- Allow you to add exception handlers to your Lambda in a easy manner, allowing to gracefully deal with exceptions.


### _Lambda_ Decorator
In order to pyckish to work it is required to add an instance of the Lambda class as a decorator above your lambda
function. That is the only requirement. But in order to your function accept parameters you have to create some
parameters in your function with type annotation.

### Extract HTTP Data from Event

Pyckish provides classes that allows you to extract HTTP Data from the event, such ass `Path`, `Method`, 
`PathParameter`, `PathParameters`, `Header`, `Headers`, `QueryParameter`, `QueryParameters` and `Body`. These classes
are all children classes of _LambdaInputElement_ class.

The version in the singular means they are going to extract only on parameter and requires 
in the type annotation only the type of that specific parameter, the ones in the plural means
they are going to extract all parameters at once, the type annotation needs to be a Pydantic Model.

Checkout the difference:
```python
import pyckish
from pyckish.http_elements import Header, Headers
import pydantic

class MyAuthHeader(pydantic.BaseModel):
    auth: str = pydantic.Field(alias='authorization')
    host: str

event = {
    'headers': {'authorization': 'token', 'host': '177.177'}
}
context = {}

@pyckish.Lambda()
def lambda_handler(
        auth: str = Header(),
        my_header: MyAuthHeader = Headers() 
) -> None:
    print(auth)
    print(my_header)

lambda_handler(event, context)
``` 


### Simple extraction from Event
If you do not provide a child of _LambdaInputElement_ class on the default value, the name of the parameter act as
a key to be extracted on the event.

```python
import pyckish

event, context = {'my_value_on_event': '200'}, {}


@pyckish.Lambda()
def lambda_handler(
        my_param_on_event: int = 500
) -> None:
    print(f'value: {my_param_on_event}, type: {type(my_param_on_event)}')


lambda_handler(event, context)
``` 

### Custom _LambdaInputElement_
If you want to extract your own value from the event or context with validation and parsing capabilities, you can
create your own _LambdaInputElement_ child class. It is required that this class implements a method called "extract"
accepting a _LambdaInput_ instance. _LambdaInput_ is just a dataclass with two attributes, event and context.
```python
import pyckish
from pyckish import LambdaInputElement, LambdaInput
from pyckish import ValidationError

class MySpecialParameter(LambdaInputElement):
    def extract(self, lambda_input: LambdaInput) -> str:
        try:
            return lambda_input.event['my_special_parameter_key']['another']
        except KeyError:
            raise ValidationError('My special parameter is missing')

@pyckish.Lambda()
def lambda_handler(
        param: str = MySpecialParameter()
) -> None:
    print(f'my param: {param}')
``` 

### Adding Exception Handlers
Exception Handlers are functions to be executed when an error occurs in your lambda. To make a function to each error
use the `add_exception_handler` method.

```python
import pyckish
from pyckish import LambdaInput

class MyException(Exception):
    pass

# This signature is required
def handler_for_my_exception(lambda_input: LambdaInput, exception: Exception) -> str:
    # this return is going to be the lambda's return value
    return 'My exception occurred'

pyckish_lambda = pyckish.Lambda()

# Here you define what function is going to be executed when the exception you pass occurs
pyckish_lambda.add_exception_handler(handler_for_my_exception, MyException)

# realize you have to use the instance you instantiated above
@pyckish_lambda
def lambda_handler() -> None:
    raise MyException()


lambda_handler({}, {})
``` 