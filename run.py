import bootstrap

if __name__ == "__main__":
    bootstrap.initialize_backend()
    bootstrap.swagger_app.run(host=bootstrap.host, port=bootstrap.port, debug=True)
