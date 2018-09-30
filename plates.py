import matplotlib
import json
import re

class Sample(object):
    def __init__(self,sample_name,exp_num,order_num):
        self.sample_name=sample_name
        self.exp_num=exp_num
        self.order_num=order_num

    def getSampleName(self):
        return self.sample_name

    def getExpNum(self):
        return self.exp_num

    def getOrderNum(self):
        return self.order_num

def sortByExp(samples_list):
    samples_dict={}
    for s in samples_list:
        if s.getExpNum() not in samples_dict:
            samples_dict[str(s.getExpNum())]=[s]
        elif s.getExpNum() in samples_dict:
            samples_dict[str(s.getExpNum())].append(s)
    return samples_dict


def readInSamplesFromJSON():
    samples_list=[]
    with open("sample_data_2.json") as json_data:
        d=json.load(json_data)
        for entry in d:
            samples_list.append(Sample(entry["name"],entry["exp"],entry["order_num"]))

    if len(samples_list)>96 or len(samples_list)==0:
        print("Invalid Sample Number, please review input file")
        exit();
    else:
        print("valid sample number")
    return samples_list

def createListForMatrix(samples_dict):
    ordered_list=[]
    temp=[]
    leftovers=[]
    for key in samples_dict:
        temp=[]
        if len(samples_dict[key])% 8==0:
            for s in samples_dict[key]:
                temp.append(s)
            ordered_list.append(temp)
        else:
            left=[]
            rows=(len(samples_dict[key])//8)
            rem=len(samples_dict[key])%8
            if rows>0 and rem!=0:
                count=0
                while count<rows*8:
                    temp.append(samples_dict[key][count])
                    count+=1
                for t in temp:
                    ordered_list.append(t)
                temp=[]
                while count<(rows*8)+rem:
                    left.append(samples_dict[key][count])
                    count+=1
                for l in left:
                    leftovers.append(l)
            elif rows==0 and rem!=0:
                count=0
                while count<(rows*8)+rem:
                    left.append(samples_dict[key][count])
                    count+=1
                for l in left:
                    leftovers.append(l)

    sorted_ex=sortByExp(leftovers)
    lf=[]
    for ex in sorted_ex:
        lf.append(sorted_ex[ex])
    combo_list=[]

    temp=[]
    no_matches=[]
    used=[]
    already_used=False
    for a in lf:
        left=8-len(a)
        for sample in a:
            temp.append(sample)
        found=False
        for b in lf:
            if len(b)==left and b!=a:
                found=True
                print("Match")
                if len(used)!=0:
                    for s in used:
                        if s[0].getExpNum()==b[0].getExpNum():
                            already_used=True
                if already_used==False:
                    for sam in b:
                        temp.append(sam)
                    used.append(b)
                    used.append(a)
                    lf.remove(b)
                    break
            else:
                found=False
        if found==True:
            combo_list.append(temp)
            temp=[]
        elif found==False:
            print("No Match")
            for sp in a:
                no_matches.append(sp)

    for c in combo_list:
        for o in c:
            ordered_list.append(o)

    for nm in no_matches:
        ordered_list.append(nm)
    return ordered_list

color_list=[]
for c in matplotlib.colors.cnames:
    color_list.append(matplotlib.colors.cnames[c])

samples_list=readInSamplesFromJSON()
samples_dict=sortByExp(samples_list)
ordered_list=createListForMatrix(samples_dict)

colored_dict={}
color_count=0
for o in ordered_list:
    colored_dict[o.getExpNum()]=color_list[color_count]
    color_count+=1
    if o.getExpNum() in colored_dict:
        num=0
    else:
        colored_dict[o.getExpNum()]=color_list[color_count]
        count+=1

template=open("platelayout_template.html","r")
colored_layout=open("platelayout.html","w")
matrix=[]
for line in template:
    l=line.split("\n")
    if l[0][:3]=="<tr":
        matrix.append(l[0])
useful_matrix=[]
for m in matrix:
    m=m.split("</td>")
    useful_matrix.append(m)

transposed=zip(*useful_matrix)
count=0
test=[]
temp=[]
while count<len(ordered_list):
    for t in transposed:
        for r in t:
            if count<len(ordered_list):
                r=r.replace("sample_color",str(colored_dict[ordered_list[count].getExpNum()]))
                r=r.replace("Sample Name",str(ordered_list[count].getSampleName()))
                r=r.replace("Exp#",str(ordered_list[count].getExpNum()))
                r=r.replace("Order#",str(ordered_list[count].getOrderNum()))
                temp.append(r)
                count+=1
            else:
                r=r.replace("sample_color","#FFFFFF")
                r=r.replace("Sample Name","Empty")
                r=r.replace("Exp#"," ")
                r=r.replace("Order#"," ")
                                                                
                temp.append(r)
                count+=1
        test.append(temp)
        temp=[]
untrans=zip(*test)

colored_layout.write("<html>")
colored_layout.write("\n")
colored_layout.write("<head>")
colored_layout.write("\n")
colored_layout.write("<style>")
colored_layout.write("\n")
colored_layout.write("table{border: 1px solid black;}")
colored_layout.write("\n")
colored_layout.write("td{border:1px solid black;}")
colored_layout.write("\n")
colored_layout.write("</style>")
colored_layout.write("\n")
colored_layout.write("</head>")
colored_layout.write("\n")
colored_layout.write("<body>")
colored_layout.write("\n")
colored_layout.write("<h1>Plate Layout</h1>")
colored_layout.write("\n")
colored_layout.write("<table>")
colored_layout.write("\n")

for u in untrans:
    for n in u:
        if n!="</tr>":
            colored_layout.write(str(n))
            colored_layout.write("</td>")
            colored_layout.write("\n")
        else:
            colored_layout.write(str(n))
            colored_layout.write("\n")

colored_layout.write("</table>")
colored_layout.write("\n")
colored_layout.write("</body>")
colored_layout.write("\n")
colored_layout.write("</html>")
colored_layout.close()









