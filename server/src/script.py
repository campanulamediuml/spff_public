from data.server import Data
from common.common import common_tools
params = {
    'username':'campanula',
    'pwhash':common_tools.get_md5('')
}
Data.insert('admin',params)
