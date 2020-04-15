from common.common import common_tools
from data.server import Data
from dbmodel import model

model.init_tables()
params = {
    'username':'test',
    'pwhash':common_tools.get_md5('123456')
}
Data.insert('admin',params)