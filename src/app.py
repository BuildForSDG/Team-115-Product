from .api.v1 import application


def run():
    application.run(debug=True)