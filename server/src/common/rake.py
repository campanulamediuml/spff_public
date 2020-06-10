import re
import operator

debug = False
test = True


def is_number(s):
    try:
        float(s) if '.' in s else int(s)
        return True
    except ValueError:
        return False


def load_stop_words(stop_word_file):
    """
    Utility function to load stop words from a file and return as a list of words
    @param stop_word_file Path and file name of a file containing stop words.
    @return list A list of stop words.
    """
    stop_words = []
    for line in open(stop_word_file):
        if line.strip()[0:1] != "#":
            for word in line.split():  # in case more than one per line
                stop_words.append(word)
    return stop_words


def separate_words(text, min_word_return_size):
    """
    Utility function to return a list of all words that are have a length greater than a specified number of characters.
    @param text The text that must be split in to words.
    @param min_word_return_size The minimum no of characters a word must have to be included.
    """
    splitter = re.compile('[^a-zA-Z0-9_\\+\\-/]')
    words = []
    for single_word in splitter.split(text):
        current_word = single_word.strip().lower()
        #leave numbers in phrase, but don't count as words, since they tend to invalidate scores of their phrases
        if len(current_word) > min_word_return_size and current_word != '' and not is_number(current_word):
            words.append(current_word)
    return words


def split_sentences(text):
    """
    Utility function to return a list of sentences.
    @param text The text that must be split in to sentences.
    """
    sentence_delimiters = re.compile(u'[.!?,;:\t\\\\"\\(\\)\\\'\u2019\u2013]|\\s\\-\\s')
    sentences = sentence_delimiters.split(text)
    return sentences


def build_stop_word_regex(stop_word_file_path):
    stop_word_list = load_stop_words(stop_word_file_path)
    stop_word_regex_list = []
    for word in stop_word_list:
        word_regex = r'\b' + word + r'(?![\w-])'  # added look ahead for hyphen
        stop_word_regex_list.append(word_regex)
    stop_word_pattern = re.compile('|'.join(stop_word_regex_list), re.IGNORECASE)
    return stop_word_pattern


def generate_candidate_keywords(sentence_list, stopword_pattern):
    phrase_list = []
    for s in sentence_list:
        tmp = re.sub(stopword_pattern, '|', s.strip())
        phrases = tmp.split("|")
        for phrase in phrases:
            phrase = phrase.strip().lower()
            if phrase != "":
                phrase_list.append(phrase)
    return phrase_list


def calculate_word_scores(phraseList):
    word_frequency = {}
    word_degree = {}
    for phrase in phraseList:
        word_list = separate_words(phrase, 0)
        word_list_length = len(word_list)
        word_list_degree = word_list_length - 1
        #if word_list_degree > 3: word_list_degree = 3 #exp.
        for word in word_list:
            word_frequency.setdefault(word, 0)
            word_frequency[word] += 1
            word_degree.setdefault(word, 0)
            word_degree[word] += word_list_degree  #orig.
            #word_degree[word] += 1/(word_list_length*1.0) #exp.
    for item in word_frequency:
        word_degree[item] = word_degree[item] + word_frequency[item]

    # Calculate Word scores = deg(w)/frew(w)
    word_score = {}
    for item in word_frequency:
        word_score.setdefault(item, 0)
        word_score[item] = word_degree[item] / (word_frequency[item] * 1.0)  #orig.
    #word_score[item] = word_frequency[item]/(word_degree[item] * 1.0) #exp.
    return word_score


def generate_candidate_keyword_scores(phrase_list, word_score):
    keyword_candidates = {}
    for phrase in phrase_list:
        keyword_candidates.setdefault(phrase, 0)
        word_list = separate_words(phrase, 0)
        candidate_score = 0
        for word in word_list:
            candidate_score += word_score[word]
        keyword_candidates[phrase] = candidate_score
    return keyword_candidates


class Rake(object):
    def __init__(self, stop_words_path):
        self.stop_words_path = stop_words_path
        self.__stop_words_pattern = build_stop_word_regex(stop_words_path)

    def run(self, text):
        sentence_list = split_sentences(text)

        phrase_list = generate_candidate_keywords(sentence_list, self.__stop_words_pattern)

        word_scores = calculate_word_scores(phrase_list)

        keyword_candidates = generate_candidate_keyword_scores(phrase_list, word_scores)
        # print(keyword_candidates)

        sorted_keywords = sorted(keyword_candidates.items(), key=operator.itemgetter(1), reverse=True)
        return sorted_keywords

if __name__=='__main__':
    rk = Rake('../etc/stop_word.txt')
    test = '''World War I (often abbreviated as WWI or WW1), also known as the First World War or the Great War, was a global war originating in Europe that lasted from 28 July 1914 to 11 November 1918. Contemporaneously described as "the war to end all wars",[7] it led to the mobilisation of more than 70 million military personnel, including 60 million Europeans, making it one of the largest wars in history.[8][9] It is also one of the deadliest conflicts in history,[10] with an estimated nine million combatants and seven million civilian deaths as a direct result of the war, while resulting genocides and the 1918 influenza pandemic caused another 50 to 100 million deaths worldwide.[11]
On 28 June 1914, Gavrilo Princip, a Bosnian Serb Yugoslav nationalist, assassinated the Austro-Hungarian heir Archduke Franz Ferdinand in Sarajevo, leading to the July Crisis.[12][13] In response, on 23 July Austria-Hungary issued an ultimatum to Serbia. Serbia's reply failed to satisfy the Austrians, and the two moved to a war footing.
A network of interlocking alliances enlarged the crisis from a bilateral issue in the Balkans to one involving most of Europe. By July 1914, the great powers of Europe were divided into two coalitions: the Triple Entente—consisting of France, Russia and Britain—and the Triple Alliance of Germany, Austria-Hungary and Italy (the Triple Alliance was primarily defensive in nature, allowing Italy to stay out of the war in 1914).[14] Russia felt it necessary to back Serbia and, after Austria-Hungary shelled the Serbian capital of Belgrade on the 28th, partial mobilisation was approved.[15] General Russian mobilisation was announced on the evening of 30 July; on the 31st, Austria-Hungary and Germany did the same, while Germany demanded Russia demobilise within 12 hours.[16] When Russia failed to comply, Germany declared war on 1 August in support of Austria-Hungary, with Austria-Hungary following suit on 6th; France ordered full mobilisation in support of Russia on 2 August.[17]
German strategy for a war on two fronts against France and Russia was to rapidly concentrate the bulk of its army in the West to defeat France within four weeks, then shift forces to the East before Russia could fully mobilise; this was later known as the Schlieffen Plan.[18] On 2 August, Germany demanded free passage through Belgium, an essential element in achieving a quick victory over France.[19] When this was refused, German forces invaded Belgium on 3 August and declared war on France the same day; the Belgian government invoked the 1839 Treaty of London and in compliance with its obligations under this, Britain declared war on Germany on 4 August.[20][21] On 12 August, Britain and France also declared war on Austria-Hungary; on the 23rd, Japan sided with the Entente, seizing German possessions in China and the Pacific. In November 1914, the Ottoman Empire entered the war on the side of the Alliance, opening fronts in the Caucasus, Mesopotamia and the Sinai Peninsula. The war was fought in and drew upon each powers' colonial empires as well, spreading the conflict to Africa and across the globe. The Entente and its allies would eventually become known as the Allied Powers, while the grouping of Austria-Hungary, Germany and their allies would become known as the Central Powers.
The German advance into France was halted at the Battle of the Marne and by the end of 1914, the Western Front settled into a battle of attrition, marked by a long series of trench lines that changed little until 1917 (the Eastern Front, by contrast, was marked by much greater exchanges of territory). In 1915, Italy joined the Allied Powers and opened a front in the Alps. The Kingdom of Bulgaria joined the Central Powers in 1915 and the Kingdom of Greece joined the Allies in 1917, expanding the war in the Balkans. The United States initially remained neutral, although by doing nothing to prevent the Allies from procuring American supplies whilst the Allied blockade effectively prevented the Germans from doing the same the U.S. became an important supplier of war material to the Allies. Eventually, after the sinking of American merchant ships by German submarines, and the revelation that the Germans were trying to incite Mexico to make war on the United States, the U.S. declared war on Germany on 6 April 1917. Trained American forces would not begin arriving at the front in large numbers until mid-1918, but ultimately the American Expeditionary Force would reach some two million troops.[22]
Though Serbia was defeated in 1915, and Romania joined the Allied Powers in 1916 only to be defeated in 1917, none of the great powers were knocked out of the war until 1918. The 1917 February Revolution in Russia replaced the Tsarist autocracy with the Provisional Government, but continuing discontent at the cost of the war led to the October Revolution, the creation of the Soviet Socialist Republic, and the signing of the Treaty of Brest-Litovsk by the new government in March 1918, ending Russia's involvement in the war. This allowed the transfer of large numbers of German troops from the East to the Western Front, resulting in the German March 1918 Offensive. This offensive was initially successful, but the Allies rallied and drove the Germans back in their Hundred Days Offensive.[23] Bulgaria was the first Central Power to sign an armistice—the Armistice of Salonica on 29 September 1918. On 30 October, the Ottoman Empire capitulated, signing the Armistice of Mudros.[24] On 4 November, the Austro-Hungarian empire agreed to the Armistice of Villa Giusti. With its allies defeated, revolution at home, and the military no longer willing to fight, Kaiser Wilhelm abdicated on 9 November and Germany signed an armistice on 11 November 1918.
World War I was a significant turning point in the political, cultural, economic, and social climate of the world. The war and its immediate aftermath sparked numerous revolutions and uprisings. The Big Four (Britain, France, the United States, and Italy) imposed their terms on the defeated powers in a series of treaties agreed at the 1919 Paris Peace Conference, the most well known being the German peace treaty—the Treaty of Versailles.[25] Ultimately, as a result of the war the Austro-Hungarian, German, Ottoman, and Russian Empires ceased to exist, with numerous new states created from their remains. However, despite the conclusive Allied victory (and the creation of the League of Nations during the Peace Conference, intended to prevent future wars), a Second World War would follow just over twenty years later.
'''
    res = rk.run(test)
    print(res)
