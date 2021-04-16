from app_demo import create_app

import os
import configparser

config = configparser.ConfigParser()
config.read(os.path.abspath(os.path.join("instance/.ini")))

if __name__ == '__main__':
    app = create_app()
    app.config['DEBUG'] = False
    app.config['APP_DB_URI'] = config['TEST']['APP_DB_URI']
    app.config['APP_NS'] = config['TEST']['APP_NS']
    app.config['SECRET_KEY'] = config['TEST']['SECRET_KEY']

    app.run(host="192.168.1.5",port=5000)