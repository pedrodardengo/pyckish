
"""This is an example of event used for testing purposes"""
EVENT_EXAMPLE = {
    'pathParameters': {
        'param_1': '200',
        'param_2': 'someRandomCharacters'
    },
    'headers': {
        'header_1': ['1', '2', '3'],
        'header_2': {4, 5, 6}
    },
    'body': {
        'body_1': {
            'body_1_1': 1.6,
            'body_1_2': '1996-15-1'
        },
        'body_2': {'1', '2', '3'}
    },
    'queryStringParameters': {
        'q_1': '1996-15-1',
        'q_3': []
    }
}
