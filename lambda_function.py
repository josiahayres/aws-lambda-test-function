import requests

def lambda_handler(event, context):
    """
    Main handler for test lambda function.
    Makes get request to jsonplaceholder and returns a dummy todo 
    """
    test_url = 'https://jsonplaceholder.typicode.com/todos/1'
    response = requests.get(test_url)

    return {
        'statusCode': response.status_code,
        'body': response.json()
    }
