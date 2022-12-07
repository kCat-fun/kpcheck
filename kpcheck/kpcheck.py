import subprocess
import sys
import os

now_path = (os.getcwd()).replace('\\','/')

args = sys.argv

# 1: .py 2: .exe
mode = 2
exe_path = __file__[:-12]
if mode == 2:
    exe_path = "C:/kpcheck"#((sys.argv[0])[:-0]).replace('\\','/')

try:
    f = open(exe_path+"/data/fileNameList.txt", 'r', encoding='UTF-8')
    # f = open("../data/fileNameList.txt", 'r', encoding='UTF-8')
except FileNotFoundError:
    print("ファイルの読み込みに失敗しました")
    print("error:", exe_path)
    input("Enterキーを押して終了してください...")
    sys.exit()

datalist = f.readlines()
f.close()

file = ""
for fn in datalist:
    if args[1].strip() == fn.strip():
        file = fn.strip()
        break

if file == "":
    print(args[1].strip(),"は存在ません\nEnterキーを押して終了してください")
    input()
    sys.exit()

# f = open(exe_path+"/data/"+file+"/answer.txt")
# f = open("../data/"+file+"/answer.txt")
f = open(exe_path+"/data/"+file+"/answer.txt", "r")
ans = f.readlines()
for n in range(len(ans)):
    ans[n] = ans[n].replace("\\n", "\n")
    ans[n] = ans[n].split(",")
f = open(exe_path+"./data/"+file+"/output.txt", "r")
# f = open("../data/"+file+"/output.txt")
out = f.readlines()
f.close()
#print(out)
exe = now_path+"/"+args[1]+'.exe'

res = []
for n in range(len(ans)):
    res.append([])
    stdin = ""
    if len(out) > 0:
        for v in out[n].split(","):
            if str(v.replace("\n", "")) != '':
                stdin+=str(v.replace("\n", ""))
                #if n < len(ans)-1:
                stdin+="\n"
    # print(stdin.encode())
    proc = subprocess.Popen(exe ,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
    proc.stdin.write(stdin.encode())
    proc.stdin.close()
    """
    try:
        result = proc.communicate(timeout=10)
        print("error:", result)
    except subprocess.TimeoutExpired:
        proc.kill()
        print("タイムアウト")
        sys.exit()
    """

    for line in proc.stdout: #1行ずつ標準出力を得る
        res[n].append(line.decode('UTF-8'))
    proc.wait() #プロセスが終わるまで待つ

num = len(ans)
flag = []
if num < len(res):
    print("出力数が多いです")
    sys.exit()
elif num > len(res):
    print("出力数が少ないです")
    sys.exit()

#print(ans)
#print(res)

for n in range(num):
    # print("res:",res[n].strip(),", ans:",ans[n].strip())
    for i in range(len(res[n])):
        res[n][i] = res[n][i].replace("\r", "")
        ans[n][i] = ans[n][i].strip("\r")
    flag.append(res[n] == ans[n])
for n in range(num):
    print(str(n+1)+": result->" + str(res[n]) + "\n   answer->" + str(ans[n]))
    print("judge:"+ str(" OK" if flag[n] else " NG"))

if flag.count(True) == num:
    print("All correct!!")
else:
    print("Not correct...")