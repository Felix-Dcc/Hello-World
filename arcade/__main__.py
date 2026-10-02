import os

from . import create_app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f' * Open http://127.0.0.1:{port} in your browser')
    app.run(host='127.0.0.1', port=port, debug=bool(os.environ.get('FLASK_DEBUG')))
