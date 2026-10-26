"""Server-side private-plugin adapter. Never instantiate in browser/model code.

The host supplies transport(url, body, headers) from its secret-bound HTTP layer.
The adapter exports model-safe tool definitions and never returns credentials.
"""
from uuid import uuid4
from .runner import CONTRACT

NAMES = {'run_assembler': 'assembler', 'run_indexer': 'indexer',
         'get_pipeline_status': 'status', 'search_index': 'search',
         'run_technician': 'technician'}


def tool_definitions():
    identity = {
        'source_id': {'type': 'string', 'format': 'uuid'},
        'manifest_id': {'type': 'string'},
        'manifest_sha': {'type': 'string', 'pattern': '^[0-9a-f]{64}$'},
    }
    tools = []
    for name, operation in NAMES.items():
        properties = dict(identity)
        if operation in {'assembler', 'indexer'}:
            properties['persist'] = {'type': 'boolean', 'default': False}
        if operation == 'search':
            properties.update(query={'type': 'string', 'maxLength': 2000}, limit={'type': 'integer', 'minimum': 1, 'maximum': 20, 'default': 10})
        if operation not in {'status', 'technician'}:
            properties['request_id'] = {'type': 'string', 'format': 'uuid', 'description': 'Keep this UUID for retries and status correlation.'}
        required = list(identity) + (['query'] if operation == 'search' else [])
        tools.append({'name': name, 'description': 'Deep/Memory only. Explicit accepted selection. Poll status after ACCEPTED; stop on review/blocked. Technician currently unavailable.',
                      'inputSchema': {'type': 'object', 'properties': properties, 'required': required, 'additionalProperties': False}})
    return tools


class ChatTools:
    def __init__(self, transport):
        # Transport injects existing Bridge bearer secret; Chat never supplies it.
        self.transport = transport

    def call(self, name, arguments):
        if name not in NAMES:
            return {'status': 'BLOCKED', 'error': 'UNKNOWN_TOOL'}
        args = dict(arguments)
        request_id = args.pop('request_id', None) or str(uuid4())
        definition = next(t for t in tool_definitions() if t['name'] == name)
        if set(args) - set(definition['inputSchema']['properties']):
            return {'status': 'BLOCKED', 'error': 'INVALID_ARGUMENTS'}
        operation = NAMES[name]
        if operation in {'assembler', 'indexer'}: args.setdefault('persist', False)
        if operation == 'search': args.setdefault('limit', 10)
        body = {**args, 'contract_version': CONTRACT, 'operation': operation}
        try:
            response = self.transport('/deep-runner/v1/tool', body, {'Idempotency-Key': request_id})
        except Exception:
            # Persist key even when transport response is lost. Never print raw errors.
            return {'status': 'UNKNOWN', 'request_id': request_id, 'error': 'TRANSPORT_UNCERTAIN', 'retry': 'Retry exact arguments with this request_id; do not create a new key.'}
        return {**response, 'tool_request_id': request_id}
