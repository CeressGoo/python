#基本的txt操作工具

#打印txt的内容
def txtprint(fileroute):
    with open(fileroute, 'r', encoding='utf-8') as file:
        file_content = file.read()
        print(file_content)

#在txt结尾出增添内容
def txtadd(fileroute, content):
    with open(fileroute, 'a', encoding = 'utf-8') as file:
        file.write(str(content) + '\n')

#将新的文本保存为txt，若该文件名已存在则覆盖其内容
def txtsave(fileroute, content):
    with open(fileroute, 'w', encoding='utf-8') as file:
        file.write(content)

#返回txt的内容
def txtread(fileroute):
    with open(fileroute, 'r', encoding='utf-8') as file:
        return file.read()

#将txt的每一行保存在一个列表中，并返回这个列表
def txttrim(fileroute):
    trim_result = []
    with open(fileroute, 'r', encoding='utf-8') as file:
        for line in file:
            trim_result.append(line.strip())
    return trim_result

#调试
if __name__ == '__main__':
    target_fileroute = 'python\\add1.txt'
    newcontent = 'hello world!\nthis is a new txt'
    txtsave(target_fileroute, newcontent)
    txtprint(target_fileroute)

