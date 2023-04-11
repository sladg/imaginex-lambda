class HandlerError(Exception):
    code: int

    def __init__(self, msg: str, code=422) -> None:
        super().__init__(msg)
        self.code = code


def error(msg: str, code=422):
    return {
        'statusCode': code,
        'body': json.dumps({'error': msg}),
        'headers': {
            'Vary': 'Accept',
            'Content-Type': 'application/json'
        }
    }