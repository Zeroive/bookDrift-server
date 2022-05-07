

config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'root',
    'database': 'drift_books'
}



# 数据库配置类
class DBConfig:
    """
        数据库迁移       python db.py db init
        创建自动迁移脚本  python db.py db migrate
        更新到数据库     python db.py db upgrade
        查看历史版本     python db.py db history
    """
    ENV = 'development'
    DEBUG = True
    HOST = "127.0.0.1"
    PORT = 3306
    USER = "root"
    PASSWORD = "root"
    NAME = "drift_books"
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{}:{}@{}:{}/{}".format(USER, PASSWORD, HOST, PORT, NAME)
    SQLALCHEMY_TRACK_MODIFICATIONS = True


# 开发环境
class DevelopmentConfig(DBConfig):
    ENV = 'development'


# 生产环境
class ProductionConfig(DBConfig):
    ENV = 'production'
