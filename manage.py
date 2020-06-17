from flask_script import Manager           # 管理app
from flask_migrate import Migrate,MigrateCommand      #数据库迁移

from newsInfo import create_app,db,models             #创建app的函数

app = create_app('develop')

#管理app
manager = Manager(app)

#迁移数据库
Migrate(app,db)
manager.add_command('db',MigrateCommand)


if __name__ == '__main__':
    manager.run()