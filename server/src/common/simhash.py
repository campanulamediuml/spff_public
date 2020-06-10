import math
import jieba
import jieba.analyse

class SimHash(object):
    jieba_mode = 0
    kshingle_mod = 1

    def __init__(self,hash_length=64,k=5,mode=jieba_mode):
        self.stop_sign = ['\t','\n','\r','，','。',' ']
        self.hash_length = hash_length
        self.k = k
        self.mode = mode
        self.split_type = {
            SimHash.jieba_mode:self.jieba_split,
            SimHash.kshingle_mod:self.k_shingle_split
        }
        # 控制器

    def jieba_split(self,string):
        seg = jieba.cut(string, cut_all=True)
        keywords = jieba.analyse.extract_tags("|".join(seg), topK=100)
        # print(keywords)
        return keywords
    # 结巴分词

    def k_shingle_split(self,string):
        shingle = set()
        for index in range(0, len(string) - self.k + 1):
            shingle.add(string[index:index + self.k])
        # shingleList.append(shingle)
        shingle_list = list(shingle)
        # print(shingle_list)
        return shingle_list
    # k-shingle分词


    def getBinStr(self, source):
        if source == "":
            return 0

        x = ord(source[0]) << 7
        m = 1000003
        mask = 2 ** 128 - 1
        for c in source:
            x = ((x * m) ^ ord(c)) & mask
        x ^= len(source)
        if x == -1:
            x = -2
        x = bin(x).replace('0b', '').zfill(64)[-64:]
        # print(source, x)
        return str(x)
        # 二进制化处理

    def simHash(self, string):
        cut_type = self.split_type[self.mode]
        keywords = cut_type(string)
        print(keywords)
        # 分词
        ret = []
        for keyword in keywords:
            binstr = self.getBinStr(keyword)
            keylist = []
            for c in binstr:
                # weight = math.sqrt(weight * 1000)
                weight = 10
                if c == "1":
                    keylist.append(int(weight))
                else:
                    keylist.append(-int(weight))
            ret.append(keylist)
        # 对列表进行"降维"
        # print(ret)
        hash_list = self.create_hash(ret)
        hash_value =  "".join(hash_list)
        # print
        return hash_value
    # 矩阵处理
    # 计算simhash
    def create_hash(self,ret):
        rows = len(ret)
        cols = len(ret[0])
        result = []
        for i in range(cols):
            tmp = 0
            for j in range(rows):
                tmp += int(ret[j][i])
            if tmp > 0:
                tmp = "1"
            elif tmp <= 0:
                tmp = "0"
            result.append(tmp)
        # print(result)
        return result
    # 哈希矩阵

    def get_distance(self, hashstr1, hashstr2):
        score = 0
        for index, char in enumerate(hashstr1):
            if char == hashstr2[index]:
                continue
            else:
                score+=1
        return score
    # 计算距离

    def check_is_sim_by_data(self,data_1,data_2,data_1_length,data_2_length):
        hash_1 = self.simHash(data_1)
        hash_2 = self.simHash(data_2)
        print(hash_1)
        print(hash_2)
        tmp_1 = ((data_1_length**2)+(data_2_length**2))
        # print(tmp_1)
        check_value = (math.sqrt((tmp_1)))/(math.sqrt(data_1_length+data_2_length))
        # 长度差异越大的文字，处理应该越宽松
        return self.check_is_sim_by_hash(hash_1,hash_2,check_value)
        # 特征值长度的算法为两个字符串长度的平方和，除以两个字符串长度和的平方根

    def check_is_sim_by_hash(self, hash_1, hash_2, check_value):
        sim_score = self.get_distance(hash_1, hash_2)
        print('汉明距离hm_distance', sim_score)
        sim_rate = 1 - (sim_score / self.hash_length)
        print('哈希相似度sim_rate', sim_rate)
        print(check_value)
        return sim_rate
        # 哈希值差异分值大于特征指标的话认为二者不相似


if __name__ == "__main__":
    simhash = SimHash()
    s1 = "天魔王米尔寇和昂哥立安联手毁了双圣树，之后精灵宝钻成了保存双圣树未毁坏前的光芒的物品，因此维拉向费诺垦求，希望他能将精灵宝钻交出，好让双圣树能复活，然而费诺拒绝了"
    s2 = "精灵宝钻成了魔王米尔寇和昂哥立安联手毁了双圣树之后，仅存的保存双圣树未毁坏前的光芒的物品，然而费诺拒绝了维拉的请求，维拉希望他能交出精灵宝钻，好复活双圣树的恳求"
    res = simhash.check_is_sim_by_data(s1,s2,len(s1),len(s2))
    print(res)
    # 基于jieba分词
    simhash = SimHash(k=2,mode=SimHash.kshingle_mod)
    s1 = "天魔王米尔寇和昂哥立安联手毁了双圣树，之后精灵宝钻成了保存双圣树未毁坏前的光芒的物品，因此维拉向费诺垦求，希望他能将精灵宝钻交出，好让双圣树能复活，然而费诺拒绝了"
    s2 = "精灵宝钻成了魔王米尔寇和昂哥立安联手毁了双圣树之后，仅存的保存双圣树未毁坏前的光芒的物品，然而费诺拒绝了维拉的请求，维拉希望他能交出精灵宝钻，好复活双圣树的恳求"
    res = simhash.check_is_sim_by_data(s1, s2, len(s1), len(s2))
    print(res)
    # 基于k-shingle