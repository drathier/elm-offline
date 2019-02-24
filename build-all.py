
import os
from pathlib import Path
from subprocess import run
import shutil
import json

root=os.path.abspath(".")
print("root", root)

# todo: find path to elm binary dynamically
# todo: clear elm-stuff automatically if it exists

def clearElmStuffs(path):
    rmDirs = []
    for dirName, subdirList, fileList in os.walk(path):
        if dirName.endswith("elm-stuff"):
            rmDirs += [dirName]
    for d in rmDirs:
        shutil.rmtree(d)


def walkElmPkgs():
    for dirName, subdirList, fileList in os.walk("./all-elm-pkg-sources/", topdown=True):
        if dirName.count("/") - root.count("/") > 2:
            #print("break", dirName)
            continue

        if os.path.exists(dirName + "/elm.json"):
            parts = dirName.split("/")
            vsn = parts[-1]
            pkgName = parts[-2]
            authorName = parts[-3]
            print()
            print("#", authorName + "/" + pkgName + "/" + vsn)

            #print(authorName, pkgName, vsn, "###", dirName, fileList, fileList)
            elmFiles = findElmFilesIn(dirName)
            #print("elmFiles", elmFiles)
            args = ["/Users/drathier/.local/bin/elm", "make"] + elmFiles
            print("args", args)
            res = run(args, env={"ELM_HOME": root+"/elm-home"}, capture_output=True, cwd=dirName)
            res.stdout and print(res.stdout.decode("utf-8"))
            res.stderr and print(res.stderr.decode("utf-8"))

            #exit(1)


def findElmFilesIn(path):
    # find elm.json and parse exposed modules
    with open(path + "/elm.json") as f:
        s = json.load(f)

        #print("s", s)
        modules = s["exposed-modules"]
        mpath = ["src/" + m.replace(".", "/") + ".elm" for m in modules]
        #print(mpath)
        return mpath


        #exit(42)



def findElmFilesIn2(relativeTo, path):
    res = []
    for dirName, subdirList, fileList in os.walk(path):
        res += [str(Path(dirName).relative_to(Path(relativeTo))) + "/" + f for f in fileList if f.endswith("elm")]
    return res

#print("cleaning elm-stuff/ dirs")
#clearElmStuffs(root + "/all-elm-pkg-sources")
print("walking")
walkElmPkgs()
