import logging
import os
from flask import Flask, jsonify, request


class APIServer:
    def __init__(self, endpoint_name, monitor_resource, monitor_resource_fields):
        self.host = "0.0.0.0"
        self.port = 8000
        self.get_resource_url = "/api/{}".format(endpoint_name)
        self.shutdown_url = "/api/shutdown"

        # endpoint name is the URL suffix that this server will listen on
        self.endpoint_name = endpoint_name

        # resource is an object that will be JSON-ified and returned whenever
        # a client makes a request via `get_resource`
        self.resource = monitor_resource
        self.resource_fields = monitor_resource_fields

        # initialize Flask app
        self.app = Flask(__name__)
        self.app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
        # mark Werkzeug as already run
        # TODO: not sure what the side effects of this are, but it prevents the
        # Flask startup message from printing to the console
        os.environ["WERKZEUG_RUN_MAIN"] = "true"

        # end endpoint to get resource
        self.app.add_url_rule(rule=self.get_resource_url,
                              endpoint="get_resource", view_func=self.get_resource)
        # end endpoint to shutdown server
        self.app.add_url_rule(rule=self.shutdown_url, endpoint="shutdown", view_func=self.shutdown)

        # Minimise console logging output
        log = logging.getLogger("werkzeug")
        log.setLevel(logging.ERROR)
        self.app.logger.disabled = True

    def _get_resource_item_fields(self, item):
        return {
            k: v for k, v in item.items()
            if k in self.resource_fields
        }

    def get_resource(self):
        ret_resource = [
            self._get_resource_item_fields(resource_item)
            for resource_item in self.resource
        ]

        return jsonify(ret_resource)

    def shutdown(self):
        print ("Shutting down API server")
        request.environ.get('werkzeug.server.shutdown')()
        return "Done"

    def run(self):
        self.app.run(debug=False, host=self.host, port=self.port)


if __name__ == "__main__":
    tasks = [
        {
            'id': 1,
            'title': u'Buy groceries',
            'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
            'done': False
        },
        {
            'id': 2,
            'title': u'Learn Python',
            'description': u'Need to find a good Python tutorial on the web',
            'done': False
        }
    ]

    server = APIServer(resource=tasks, endpoint_name="tasks")
    server.run()
