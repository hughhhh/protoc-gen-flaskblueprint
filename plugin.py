#!/usr/bin/env python
from collections import defaultdict
import sys
import itertools
import json

# Example for looking up docs: https://developers.google.com/protocol-buffers/docs/reference/python/google.protobuf.descriptor_pb2.FileDescriptorProto
from google.protobuf.compiler import plugin_pb2 as plugin
from google.protobuf.descriptor_pb2 import DescriptorProto, EnumDescriptorProto, ServiceDescriptorProto, MethodDescriptorProto

def traverse(proto_file):
    def _traverse(package, items):

        for item in items:
            yield item, package
            if isinstance(item, DescriptorProto):
                for enum in item.enum_type:
                    yield enum, package

                for nested in item.nested_type:
                    nested_package = package + item.name

                    for nested_item in _traverse(nested, nested_package):
                        yield nested_item, nested_package

            if isinstance(item, MethodDescriptorProto):
                print(type(item))
    # https://developers.google.com/protocol-buffers/docs/reference/python/google.protobuf.descriptor_pb2.FileDescriptorProto-class
    return itertools.chain(
        _traverse(proto_file.package, proto_file.enum_type),
        _traverse(proto_file.package, proto_file.message_type),
        _traverse(proto_file.package, proto_file.service),
    )

def generate_code(request, response):
    for proto_file in request.proto_file:
        output = defaultdict(list)
        # Parse request
        for item, package in traverse(proto_file):
            proto_type = None
            try:
                name = item.name
            except Exception:
                name = 'no name'

            data = {
                'package': proto_file.package or '&lt;root&gt;',
                'filename': proto_file.name,
                'name': name,
            }

            if isinstance(item, DescriptorProto):
                proto_type = 'messages'
                data.update({
                    'type': 'Message',
                    'properties': [{'name': f.name, 'type': int(f.type)}
                                   for f in item.field]
                })

            elif isinstance(item, EnumDescriptorProto):
                proto_type = 'enums'
                data.update({
                    'type': 'Enum',
                    'values': [{'name': v.name, 'value': v.number}
                               for v in item.value]
                })

            elif isinstance(item, ServiceDescriptorProto):
                """
                todo(hugh): Figure out how to traverse the http options section
                right now the options json is empty and not returning anything
                """
                proto_type = 'services'
                data.update({
                    'type': 'Service',
                    'methods': [{'name': rpc.name, 'input': rpc.input_type,
                                 'output': rpc.output_type}
                                for rpc in item.method],
                    'options': None,
                })

            output[proto_type].append(data)

        # Fill response
        f = response.file.add()
        f.name = proto_file.name + '.json'
        f.content = json.dumps(output, indent=2)


if __name__ == '__main__':
    # Read request message from stdin
    data = sys.stdin.read()

    # Parse request
    request = plugin.CodeGeneratorRequest()
    request.ParseFromString(data)

    # Create response
    response = plugin.CodeGeneratorResponse()

    # Generate code
    generate_code(request, response)

    # Serialise response message
    output = response.SerializeToString()

    sys.stdout.write(output)
