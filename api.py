import logging
import os
from flask import Flask, jsonify, request

class APIServer:
    def __init__(self, resource, endpoint_name):
        self.resource = resource
        self.endpoint_name = endpoint_name

        # initialize Flask app
        self.app = Flask(__name__)
        self.app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
        # mark Werkzeug as already run
        # TODO: not sure what the side effects of this are, but it prevents the
        # Flask startup message from printing to the console
        os.environ["WERKZEUG_RUN_MAIN"] = "true"

        # end endpoint to get items
        self.app.add_url_rule(rule="/api/{}".format(endpoint_name), endpoint="get_resource", view_func=self.get_tasks)
        # end endpoint to shutdown server
        self.app.add_url_rule(rule="/api/shutdown", endpoint="shutdown", view_func=self.shutdown)

        # Minimise console logging output
        log = logging.getLogger("werkzeug")
        log.setLevel(logging.ERROR)
        self.app.logger.disabled = True

    def get_tasks(self):
        return jsonify(self.resource)

    def shutdown(self):
        print ("Shutting down API server")
        request.environ.get('werkzeug.server.shutdown')()
        return "Done"

    def run(self):
        self.app.run(debug=False, host="0.0.0.0", port=8000)

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
