# Pyckish
### AWS Lambda Event extractor/parser/validator" 
Pyckish is an "extract, parse and validate" solution to allow ease of use when dealing with AWS Lambdas.

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
from my_models import Item

@pyckish.AWSEventExtractor()
def lambda_handler(
        auth: str = HTTPHeader(alias='authorization_token'),
        store: str = HTTPPathParameter(default='my_store'),
        item: Item = HTTPBody()
) -> float:
    user = get_user(auth)
    price = get_price(item.dict(), store, user)
    return price
```

And get validation and parsing free of trouble thanks to integration with Pydantic.
