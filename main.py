import logging
from app import init_app

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    app = init_app()

    app.run(host='0.0.0.0', port=5000, debug=True)
