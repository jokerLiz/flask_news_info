from flask_script import Manager           # 管理app
from flask_migrate import Migrate,MigrateCommand      #数据库迁移
from flask import session
from newsInfo import create_app,db

app = create_app('develop')

#管理app
manager = Manager(app)

#迁移数据库
Migrate(app,db)
manager.add_command('db',MigrateCommand)


@app.route('/')
def index():
    session['name2'] = 'lizhao2'
    return 'index1'


if __name__ == '__main__':
    manager.run()