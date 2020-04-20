from werkzeug.security import generate_password_hash

from common.common import common_tools
from data.server import Data



def admin():
    Data.query('drop table admin')
    colums = [
        ('id', 'int', 'AUTO_INCREMENT', 'primary key'),
        ('username', 'varchar(128)','default ""'),
        # 用户名
        ('pwhash', 'varchar(512)','default ""'),
        # 密码哈希
        ('token','varchar(128)','default ""'),
        # token
        ('auth_id','int','default 1'),
        # 权限
        ('c_time', 'int', 'default "0"'),
        # 创建时间
        ('u_time', 'int', 'default "0"'),
        # 更新时间
        ('comment', 'varchar(1024)', 'default ""'),
        # 备注
        ('status', 'int', 'default "0"'),
        # 状态
    ]
    Data.create('admin', colums)


def player():
    Data.query('drop table player')
    colums = [
        ('id', 'int', 'AUTO_INCREMENT', 'primary key'),
        ('open_id', 'varchar(128)', 'default ""'),
        # openid
        ('union_id', 'varchar(128)', 'default ""'),
        # unionid
        ('phone', 'varchar(128)', 'default ""'),
        # 电话
        ('birth_day', 'varchar(128)', 'default ""'),
        # 出生日期
        ('nickname', 'varchar(128)', 'default ""'),
        # 昵称
        ('sex', 'int', 'default "0"'),
        # 性别
        ('add_time', 'int', 'default "0"'),
        # 创建时间
        ('avatar', 'varchar(512)', 'default ""'),
        # 头像
        ('status', 'int', 'default "0"'),
        # 状态
    ]
    Data.create('player', colums)
    # 用户账号


def operate():
    # 存储后台操作记录
    Data.query('drop table admin_operate_record')
    colums = [
        ('id', 'int', 'AUTO_INCREMENT', 'primary key'),
        # 主键
        ('operater_id', 'int', 'default "0"'),
        # 操作者id
        ('operate_time', 'int', 'default "0"'),
        # 操作时间

    ]
    Data.create('admin_operate_record', colums)


def case_info():
    Data.query('drop table case_info')
    colums = [
        ('id','int', 'AUTO_INCREMENT', 'primary key'),
        ('user_id','int','default "0"'),
        ('c_time','int','default "0"'),
        ('title', 'text'),
        ('content', 'text'),
        ('is_show', 'int', 'default "1"'),
        ('content_md5', 'varchar(128)', 'default ""'),
        ('event_time','int','default "0"'),
        ('is_verified','int','default "0"'),

    ]
    Data.create('case_info', colums)

def case_post_item():
    Data.query('drop table case_post_item')
    colums = [
        ('id','int', 'AUTO_INCREMENT', 'primary key'),
        ('case_id','int','default "0"'),
        ('post_item', 'varchar(4096)', 'default ""'),
        ('c_time', 'int', 'default "0"'),
        ('is_download','int', 'default "0"'),
        ('raw_url', 'varchar(4096)', 'default ""'),

    ]
    Data.create('case_post_item', colums)

def case_search_index():
    Data.query('drop table case_search_index')
    colums = [
        ('id','int', 'AUTO_INCREMENT', 'primary key'),
        ('case_id','int','default "0"'),
        ('keyword', 'varchar(4096)', 'default ""'),
        ('keyword_md5', 'varchar(512)', 'default ""'),
    ]
    Data.create('case_search_index', colums)


def refresh_table(table_name,table_struct):
    Data.query('drop table '+table_name)
    Data.create(table_name, table_struct)



def init_tables():
    admin()
    player()
    operate()
    case_info()
    case_post_item()
    case_search_index()

if __name__=='__main__':
    init_tables()