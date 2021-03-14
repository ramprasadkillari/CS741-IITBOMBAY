from sys import exit
T 	 = 3
N 	 = 9
perm = [0,3,6,1,4,7,2,5,8]
S 	 = 3
Sbox = [0,2,4,6,3,1,7,8]
maxbias = 0
bestpath = []

mem = {}

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
	i = int(i,2)
	j = int(j,2)
	cntzeros = 0
	comb = 1<<S
	for it in range(comb):
		x = Sbox[it]
		if(allxor(it&i)^allxor(Sbox[it]&j) == 0):
			cntzeros += 1
	ans = cntzeros/comb - 0.5
	mem[i+j] = ans
	return ans

def rowbias(i,j):
	i = bin(i)[2:]
	i = '0'*(N-len(i))+i
	j = bin(j)[2:]
	j = '0'*(N-len(j))+j
	ans = 1
	for k in range(N//S):
		tmp = i[k*S:(k+1)*S]
		if(tmp=='0'*S):
			continue
		ans = 2*bias(tmp,j[k*S:(k+1)*S])
	return ans/2

def check(i,j):
	i = bin(i)[2:]
	i = '0'*(N-len(i))+i
	j = bin(j)[2:]
	j = '0'*(N-len(j))+j
	for k in range(N//S):
		if( (i[k*S:(k+1)*S]!='0'*S and j[k*S:(k+1)*S]=='0'*S) or (i[k*S:(k+1)*S]=='0'*S and j[k*S:(k+1)*S]!='0'*S) ):
			return False
	return True

def permfunc(inp2):
	out1 = bin(inp2)[2:]
	out1 = '0'*(N-len(out1))+out1
	out2 = ['0' for _ in range(N)]
	for ind in range(N):
		if(out1[ind]=='1'):
			out2[perm[ind]] = '1'

	return int("".join(out2),2)

def func(inp,round,bias,path):
	path.append(inp)
	global maxbias
	global bestpath
	if(abs(bias)<abs(maxbias)):
		return
	
	if(round>T):
		if(abs(bias)>abs(maxbias)):
			maxbias = bias
			bestpath = path.copy()
			# print("final : ",path)
			# print(bestpath)
			# path = []
		return

	comb = 1<<N
	for j in range(1,comb):
		if(not(check(inp,j))):
			continue

		tmp = rowbias(inp,j)
		if(tmp==0):
			continue
		# print(round,":",inp,j,tmp)
		out = permfunc(j)
		func(out,round+1,2*bias*tmp,path)
		path.pop()

def subgraph(path):
	res = []
	p = path[0]
	p = bin(p)[2:]
	p = '0'*(N-len(p))+p
	for i in range(N):
		if(p[i]=='1'):
			res.append("P"+str(i))
			res.append("K0"+str(i))
			# res.append("K0"+str(i))
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
	# T 	 = int(input())
	# N 	 = int(input())
	# perm = list(map(int,input().split()))
	# S 	 = int(input())
	# sbox = list(map(int,input().split()))

	comb = 1<<N

	for i in range(1,comb):
		path = []
		func(i,1,0.5,path)
		# print(bestpath)

		# if(len(bestpath)!=(T+1)):
		# 	exit()

		print(i,":",maxbias)
		# print(subgraph(bestpath))

	# print(bestpath)
	print("maxbias : ",maxbias)
	print(subgraph(bestpath))