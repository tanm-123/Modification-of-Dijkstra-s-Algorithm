class Maxheap:
    def __init__(self):
        self.list=[]
        self.index=[]#list for storing the position of each vertex in the heap
    def is_empty(self):
        if len(self.list)==0:
            return True
        else:
            return False
    def heap_up(self,n,i): #to traverse from nth node to the root 
        while self.list[(n-1)//2][0]<self.list[n][0]:# if we are at nth node then its parent node is (n-1)//2 so if parent c is less than node then we will exchange
            c1=self.list[(n-1)//2]
            c2=self.list[n]
            z=c1[1]
            y=c2[1]
            c=self.index[y]
            self.index[y]=self.index[z]
            self.index[z]=c # updating in the index list
            self.list[n]=c1
            self.list[(n-1)//2]=c2
            n=(n-1)//2
            if n==0:# means we are at root so no parent
                return
    def heap_down(self,n,i):# to traverse from node to the end of list 
        l=len(self.list)
        if n>(l-2)//2:# means we are in the leaf so no more child branches
            return
        if 2*n+2<=l-1:# if we are at nth node then 2n+1 is left child and 2n+2 is right branch
            while (self.list[2*n+1][0]>self.list[n][0] or self.list[2*n+2][0]>self.list[n][0]): #compare between child and node if child's c is more then exchange
                if  self.list[2*n+1][0]>self.list[2*n+2][0]:
                    v=self.list[2*n+1]
                else:                       #assign v with the branch having more c
                    v=self.list[2*n+2]
                c1=self.list[n]
                c2=v
                z=c1[1]
                y=c2[1]
                c=self.index[y]
                self.index[y]=self.index[z]
                self.index[z]=c
                self.list[n]=c2
                if self.list[2*n+1][0]>self.list[2*n+2][0]:
                    self.list[2*n+1]=c1
                    n=2*n+1
                else:
                    self.list[2*n+2]=c1
                    n=2*n+2
                if n>(l-2)//2:
                    break
                if 2*n+2>l-1:
                    break
        if 2*n+1<=l-1:
            if (self.list[2*n+1][0]>self.list[n][0]):
                c1=self.list[n]
                c2=self.list[2*n+1]
                z=c1[1]
                y=c2[1]
                c=self.index[y]
                self.index[y]=self.index[z]
                self.index[z]=c
                self.list[2*n+1]=c1
                self.list[n]=c2
    def insert(self,data): 
        self.list.append(data)
        if len(self.list)>1:
            self.heap_up(len(self.list)-1,data[1])
    def extractmin(self):
        t=self.list[0][1]
        self.index[t]=-1
        l=[]
        n=len(l)
        if len(self.list)>1:
            c=self.list[0]
            d=self.list.pop()
            self.list[0]=d
            s=d[1]
            self.index[s]=0
            if len(self.list)>1:
                self.heap_down(n,self.list[n][1])
        else:
            c=self.list[0]
            self.list.pop()
        return c
    def indexlist(self,l):
        self.index=l
    def changekey(self,u,a,b,c):
        self.list[u][0]=a
        self.list[u][2]=b
        self.list[u][3]=c
        if u!=0:
            self.heap_up(u,self.list[u][1])
    def givenode(self,v):
        return self.index[v]
    def givevalue(self,v):
        return self.list[v][0]
class Graph():
    def __init__(self,l,e):
        self.l=l #list storing list of all adjacent vertices,c  to index of the vertex 
        self.e=e # list storing the edges information
    def adjacencylist(self):
        n=len(self.e)
        for i in range (0,n):
            x=self.e[i][0]
            y=self.e[i][1]
            c=self.e[i][2]
            self.l[x].append((y,c))
            self.l[y].append((x,c))
    def adjacent(self,v):
        return self.l[v]
def findMaxCapacity(n,l,s,t):
    mh=Maxheap()
    ans=[t]
    r=[]# this list is made to find the route...it is a list of list of 2 things, the vertex and its previous vertex.
    for i in range (0,n):
        r.append([i,-1])# so initially we set the value of all previous vertices to -1....o(n)
    q=[]
    for i in range (0,n):
        q.append([])
    g=Graph(q,l)
    g.adjacencylist()
    list=[]#initially we set the index of each vertex as the vertex no. itself
    for i in range (0,n):
        list.append(i)
    mh.indexlist(list)
    for i in range (0,n):#in heap initially we set the source c to be 0 and rest all c to be -1 so that source is at root
        if i==s:
            mh.insert([0,i,0,0])# in heap we store 4 things(c,vertex,previous vertex, min c in that path)..initially we set the 3 and 4 parameter to 0
        else:
            mh.insert([-1,i,0,0])
    f=mh.extractmin()# this gives us source
    r[f[1]]=[f[1],f[2]] 
    p=g.adjacent(f[1]) # we find adjacent vertices to source and modify their 4 parameters
    for i in range (0,len(p)):
        h=mh.givenode(p[i][0])
        k=mh.givevalue(h)
        if p[i][1]>k:
            mh.changekey(h,p[i][1],f[1],p[i][1])
    while mh.is_empty()!=True:#order mlogn as heap stores the number of vertices
        f=mh.extractmin() #o(logn)
        r[f[1]]=[f[1],f[2]]
        if f[1]==t:
            c=f[3]
            break
        p=g.adjacent(f[1])
        for i in range (0,len(p)):# this will iterate maximum m times-> o(mlogn)
            h=mh.givenode(p[i][0])
            if h==-1:
                continue
            k=mh.givevalue(h)
            if p[i][1]>k:
                mh.changekey(h,p[i][1],f[1],min(f[3],p[i][1]))#o(logn)
    ans.append(f[2])
    j=f[2]
    while j!=s:
        ans.append(r[j][1])
        j=r[j][1]
    route=[]
    for i in range (len(ans)-1,-1,-1):
        route.append(ans[i])
    return (c,route)