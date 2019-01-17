from collections import defaultdict
from cookiecutter.main import cookiecutter
from halo import Halo
from pprint import pprint

# todo: Make this a param in that can be set after reading a proto
import hellomars_pb2
proto_descriptor = hellomars_pb2.DESCRIPTOR

spinner = Halo(text='Loading', spinner='dots')
spinner.start()

services_map = defaultdict(list)
for k, v in proto_descriptor.services_by_name.items():
    for message in v.methods:
        service = {
            'service_name': k,
            'message_name': message.name,
            'input': message.input_type.name,
            'output': message.output_type.name
        }

    # todo: Figure out how generate typing and output from endpoint
    # for field in message.input_type.fields:
    #     print(field.name)
    #     print(field.message_type)
    # for field in message.output_type.fields:
    #     print(field.name)
    #     print(field.message_type)

    services_map['buffer'].append(service)

spinner.text = 'Creating a project'
cookiecutter('flask-blueprint/',
             no_input=True,
             overwrite_if_exists=True,
             extra_context={'services': services_map}) # extra context will overwrite whatever is in cookiecutter.json

# Update message on spinner
spinner.stop()
