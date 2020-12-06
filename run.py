import bootstrap
from configuration import host, port, debug

if __name__ == "__main__":
    bootstrap.initialize_backend()
    bootstrap.swagger_app.run(host=host, port=port, debug=debug)
