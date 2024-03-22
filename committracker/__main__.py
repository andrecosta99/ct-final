from . import app


def main():
    app.run_server(debug=True)
    app.config.suppress_callback_exceptions = True


if __name__ == "__main__":
    main()
