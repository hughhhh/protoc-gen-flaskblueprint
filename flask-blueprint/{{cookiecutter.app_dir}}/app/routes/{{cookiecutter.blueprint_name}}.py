from flask import Blueprint, jsonify, request

{% for service in cookiecutter.services.buffer %}
blueprint = Blueprint("{{service.service_name}}", __name__)

@blueprint.route("/api/hello", methods=["GET"])
def {{service.message_name}}():
    # your data transformation logic should go in here.
    # Business logic should be made into new modules and called from the endpoint.
    name = "Hugh"
    # package_name.{{service.output}}()
    return jsonify({"msg": "Hello there, {}!".format(name or "world")})

{% endfor %}
