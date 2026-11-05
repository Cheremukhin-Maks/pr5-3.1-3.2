"""Точка входу для запуску сервера."""

import os
from pr5_3 import create_app

app = create_app('development')

if __name__ == '__main__':
   
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5000'))
    except ValueError:
        PORT = 5000

    HOST = os.environ.get('SERVER_HOST', '127.0.0.1')
    
    app.run(host=HOST, port=PORT, debug=True)