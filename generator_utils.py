import os
import fnmatch
import gzip, bz2
import io
import itertools
import chardet

#import time

# TODO: it's too time consuming....
def check_encoding(path):
    #start_time = time.time()
    f = io.open(path, 'rb')
    contents = f.read()
    f.close()
    chdt = chardet.detect(contents)
    #print(chdt)
    #print("--- %s seconds ---" % (time.time() - start_time))
    return chdt["encoding"]

def gen_find(filepatlist, top):
    for path, dirlist, filelist in os.walk(top):
        for i in filepatlist:
            for name in fnmatch.filter(filelist, i):
                fullpath = os.path.join(path, name)
                enc = check_encoding(fullpath)
                yield {"path": fullpath, "encoding": enc}

def gen_open(filenames):
    for name in filenames:
        path = name["path"]
        enc = name["encoding"]
        if path.endswith(".gz"):
            yield gzip.open(path)
        elif path.endswith(".bz2"):
            yield bz2.BZ2File(path)
        else:
            yield io.open(path, 'rt', encoding=enc)
            #yield open(name, 'rt', encoding='utf8')

def gen_close(filenames):
    for name in filenames:
        name.close()

def gen_cat(sources):
    for s in sources:
        try:
            for idx,item in enumerate(s):
                #yield item
                #yield str(s.name) + ":" + str(idx+1) + ":" + item
                yield {"file":s.name, "line":idx+1, "data":item}
        except:
            print("gen_cat() error: %s" % s)

def gen_grep(patc, lines):
    # patc = re.compile(pat)
    """

    :rtype: object
    """
    for line in lines:
        m = patc.search(line["data"])
        if m:
            #print("search:", m.group(0).lower())
            line['keyword'] = m.group(0).lower()
            yield line

class GeneratorLen(object):
    def __init__(self, gen, length):
        self.gen = gen
        self.length = length

    def __len__(self):
        return self.length

    def __iter__(self):
        return self.gen

    def __call__(self):
        return itertools.islice(self.gen(), self.length)