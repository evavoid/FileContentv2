import os, re

class FileNode():
    def __init__(self,current_path,rulses_package):
        self.current_path=current_path#当前节点路径
        self.rulses_package=rulses_package
        self.subnode=[]

    def load(self):
        for i in os.listdir(self.current_path):#遍历该文件夹下所有文件和文件夹
            if os.path.isdir(self.current_path+i):#如果是文件夹
                self.subnode.append(FileNode(self.current_path+i+'/',self.rulses_package))
                self.subnode[-1].load()
            else:
                if self.rules_match(i):
                    self.subnode.append(FileNode(self.current_path+i,self.rulses_package))
    def simple_show(self):
        if self.subnode:
            for i in self.subnode:
                i.simple_show()
        else:
            temp=self.current_path.split('/')
            if temp[-1]!='':
                print(self.current_path)

    def tree_show(self,layer=0):
        temp=self.current_path.split('/')
        temp=temp[-1] if temp[-1] else temp[-2]
        print("     "*layer+"|"+temp)#打印当前文件夹信息
        for i in self.subnode:
            i.tree_show(layer+1)

    def simplify(self):
        temp=[]
        for i in self.subnode:
            if os.path.isdir(i.current_path) and len(i.subnode)==0:#如果i是个空文件夹
                temp.append(i)
        for i in temp:
            self.subnode.remove(i)
        for i in self.subnode:
            i.simplify()
    """         
    def simplify(self):
        temp=[]
        for i in self.subnode:
            if os.path.isdir(i.current_path) and len(i.subnode)==0:#如果i是个空文件夹
                temp.append(i)
        if temp:#确实要移除，也就是说确实是空文件夹
            if len(temp)==len(self.subnode):#清空
                pass
            else:
                for i in temp:
                    self.subnode.remove(i)
                for i in self.subnode:
                    i.simplify()
    """
            
    def rules_match(self,filename):
        if self.rulses_package[0]==0:
            for i in self.rulses_package[1]:
                if re.match(i,filename):
                    break
            else:
                return False
            for i in self.rulses_package[2]:
                if re.match(i,filename):
                    return False
            else:
                return True
        elif self.rulses_package[0]==1:
            for i in self.rulses_package[2]:
                if re.match(i,filename):
                    break
            else:
                return True
            for i in self.rulses_package[1]:
                if re.match(i,filename):
                    return True
            else:
                return False
        

class FileContent():
    def __init__(self):
        #文件树
        self.filetree=0;
        
        #文件树起始路径
        self.startpath=0;

        #0默认拒绝
        #检索允许列表，如果没有匹配到，那么拒绝，如果匹配到了，那么检索拒绝列表
        #检索拒绝列表，如果没有匹配到，那么允许，如果匹配到了，那么拒绝
        #1默认允许
        #检索拒绝列表，如果没有匹配到，那么允许，如果匹配到了，那么检索允许列表
        #检索允许列表，如果没有匹配到，那么拒绝，如果匹配到了，那么允许
        self.mode=0;

        #规则列表，里面指定的正则表达式规则都是针对完整文件路径的
        self.accept_rules=[];
        self.reject_rules=[];

        #显示折叠，如果超过了数目就会折叠打印结果为...
        self.filefold=20;

    def set_startpath(self,startpath):
        self.startpath=str(startpath).replace("\\","/")
        if self.startpath[-1] !='/':
            self.startpath=self.startpath+'/'

    def set_mode(self,mode):
        if mode=="MODE_RAR":
            self.mode=0;
        elif mode=="MODE_ARA":
            self.mode=1;  

    def set_rules(self,rule,rule_type):
        if rule_type=="REJECT_RULE":
            self.reject_rules.append(str(rule).replace("\\","/"))
        elif rule_type=="ACCEPT_RULE":
            self.accept_rules.append(str(rule).replace("\\","/"))   

    def set_filefold(self,filefold):
        self.filefold=filefold

    def return_setting(self):
        return (self.startpath,self.mode,self.accept_rules,self.reject_rules,self.filefold)

    def get_setting(self):
        self.startpath=package[0]
        self.mode=package[1]
        self.accept_rules=package[2]
        self.reject_rules=package[3]
        self.filefold=package[4]

    def filetree_update(self):
        setting=self.return_setting()
        self.filetree=FileNode(setting[0],setting[1:4])
        self.filetree.load()

    def show(self,mode):
        if mode=='SAMPLE':
            self.filetree.simple_show()
        elif mode=='TREE':
            self.filetree.tree_show()
        elif mode[:12]=='SAMPLE_TREE_':
            for i in range(int(mode[12:])):
                self.filetree.simplify()
            self.filetree.tree_show()

if __name__=='__main__':
    cont=FileContent()

    cont.set_startpath(os.getcwd())
    cont.set_mode("MODE_RAR")
    cont.set_filefold(20)

    #往允许筛选表里写入规则，检索后缀为docx和pdf的文件
    cont.set_rules("(.*).(docx|txt)","ACCEPT_RULE")
    #往拒绝筛选表里写入规则
    cont.set_rules("(.*)简介(.*)","REJECT_RULE")
    
    cont.filetree_update()
    cont.show('SAMPLE_TREE_11')
    x=input()
