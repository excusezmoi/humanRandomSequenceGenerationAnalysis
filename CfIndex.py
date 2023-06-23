from collections import Counter

def elementPlacing(li):
    dic = {}
    for order, element in enumerate(li):
        dic.setdefault(element, []).append(order)
    return dic

def intervalCalc2(dic):
    interval = [i - j for alternative in dic for i in dic[alternative] for j in dic[alternative] if i > j]
    return interval

def countInstances(lis):
    return dict(Counter(lis))

def sumOccurences(countdict, le):
    return sum(countdict.values()) / le

def CfIndex(li):
    return sumOccurences(countInstances(intervalCalc2(elementPlacing(li))),len(li))

if __name__ == "__main__":
    li = [1,1,1,1,1,1,1,1,1,1]
    print(CfIndex(li))