from sys import exit
import itertools


maxbias = 0
bestpath = []
ls_basic = []
mem = {}
rowmem = {}
cache = {}

T 	 = 3
N 	 = 9
perm = [0,3,6,1,4,7,2,5,8]
S 	 = 3
Sbox = [0,2,4,6,3,1,7,5]

# T = 3
# N = 16
# S = 4

# Sbox = (
#     0x0E, 0x04, 0x0D, 0x01, 
# 	0x02, 0x0F, 0x0B, 0x08, 
# 	0x03, 0x0A, 0x06, 0x0C, 
# 	0x05, 0x09, 0x00, 0x07
# )

# perm = (
#     0, 4, 8, 12, 
# 	1, 5, 9, 13,
# 	2, 6, 10,14,
# 	3, 7, 11,15
# )

# T 	 = 3
# N 	 = 9
# perm = [0,3,6,1,4,7,2,5,8]
# S 	 = 3
# Sbox = [5,7,3,2,6,0,4,1]

# T 	 = 1
# N 	 = 4
# perm = [0,1,2,3]
# S 	 = 2
# Sbox = [2,1,3,0]

# T 	 = 2
# N 	 = 4
# perm = [0,1,2,3]
# S 	 = 2
# Sbox = [2,1,3,0]	

def allxor(x):
	ans = 0
	while(x!=0):
		ans ^= (x&1)
		x >>= 1
	return ans

def bias(i,j):
	if(i+j in mem):
		return mem[i+j]
	i1 = int(i,2)
	j1 = int(j,2)
	cntzeros = 0
	comb = 1<<S
	for it in range(comb):
		x = Sbox[it]
		if(allxor(it&i1)^allxor(Sbox[it]&j1) == 0):
			cntzeros += 1
	ans = cntzeros/comb - 0.5
	mem[i+j] = ans
	# if(ans==0.5):
	# 	print(i,j,ans)
	return ans

def rowbias(i,j):

	if(i+j in rowmem):
		return rowmem[i+j]
	ans = 0.5
	for k in range(N//S):
		tmp = i[k*S:(k+1)*S]
		if(tmp=='0'*S):
			continue
		ans *= 2*bias(tmp,j[k*S:(k+1)*S])
	rowmem[i+j] = ans
	return ans

def permfunc(out1):
	out2 = ['0' for _ in range(N)]
	for ind in range(N):
		if(out1[ind]=='1'):
			out2[perm[ind]] = '1'
	return "".join(out2)

def func(inp,round,localmaxbias):
	if((inp,round) in cache):
		return cache[(inp,round)]
	
	if(round>T):
		return 0.5,[int(inp,2)]

	# print(inp,round,cnt)
	comb = 1<<N
	localmaxbias = 0
	localpath = []

	somelists = []
	for k in range(N//S):
		if(inp[k*S:(k+1)*S]!='0'*S):
			somelists.append(ls_basic)
		else:
			somelists.append(['0'*S])

	for item in itertools.product(*somelists):
		j = "".join(item)

		tmp = rowbias(inp,j)
		if(tmp==0 or abs(tmp)<abs(localmaxbias)):
			continue

		out = permfunc(j)
		ans,path = func(out,round+1,localmaxbias)
		ans *= 2*tmp
		if(abs(ans)>abs(localmaxbias)):
			localmaxbias = ans
			localpath = path.copy()

	cache[(inp,round)] = (localmaxbias,[int(inp,2)]+localpath)
	return localmaxbias,[int(inp,2)]+localpath

def subgraph(path):
	res = []
	p = path[0]
	p = bin(p)[2:]
	p = '0'*(N-len(p))+p
	for i in range(N):
		if(p[i]=='1'):
			res.append("P"+str(i))
			res.append("K0"+str(i))

	for i in range(1,T):
		k = path[i]
		k = bin(k)[2:]
		k = '0'*(N-len(k))+k
		for j in range(N):
			if(k[j]=='1'):
				res.append("K"+str(i)+str(j))

	c = path[-1]
	c = bin(c)[2:]
	c = '0'*(N-len(c))+c
	for i in range(N):
		if(c[i]=='1'):
			res.append("C"+str(i))

	return ",".join(res)

if __name__ == "__main__":
	T 	 = int(input())
	N 	 = int(input())
	perm = list(map(int,input().split()))
	S 	 = int(input())
	sbox = list(map(int,input().split()))

	pows = 1<<S
	ls_basic = ['0'*(S-len(bin(i)[2:]))+bin(i)[2:] for i in range(1,pows)]
	
	comb = 1<<N
	localmaxbias = 0
	bestpath = []
	for i in range(1,comb):
		i2 = bin(i)[2:]
		i2 = '0'*(N-len(i2))+i2

		localbias,path = func(i2,1,localmaxbias)
		
		if(abs(localbias)>abs(localmaxbias)):
			localmaxbias = localbias
			bestpath = path.copy()
		print(i,":",localbias)

	print("maxbias : ",localmaxbias)
	print(subgraph(bestpath))
