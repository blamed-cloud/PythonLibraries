#!/usr/bin/python
#math_lib.py
###USAGE### math_lib.py ; sms=N ; $#=0
import re
import math
import prgm_lib

unzip=prgm_lib.unzip

op_preced_d=dict({'^': 5, '!': 4, '*': 3, '/': 3, '%': 3, '+': 2, '-': 2, '=': 1})
op_left_assoc_d=dict({'^': True, '!': False, '*': True, '/': True, '%': True, '+': True, '-': True, '=': False})
op_arg_count_d=dict({'^': 2, '!': 1, '*': 2, '/': 2, '%': 2, '+': 2, '-': 2, '=': 2})
op_list='^!*/%+-='

def get_term_len(rpn_list):
	termlens=[]
	if type(rpn_list) is list:
		termlens.append(len(prgm_lib.unzip(rpn_list)))
		termlens.append(get_term_len(rpn_list[0]))
	else:
		termlens=[1]
	return unzip(termlens)

def poly_str_coefs(string):
	output=sya(string)
	answer=const_folding(output,False)
#	print answer
	termlens=get_term_len(answer[0])
	termlens.append(0)
#	print termlens
	slices=[int(x) for x in reversed(termlens)]
	ans=unzip(answer)
	terms=[ans[slices[k-1]:slices[k]] for k in range(1,len(slices))]
	coefs=[]
#	print terms
	for k in terms:
		if k[-1]=='-':
			coefs.append(float(eval('-1*'+str(k[0]))))
		else:
			coefs.append(float(k[0]))
	return coefs
#	output=[int(x) for x in reversed(unzip(get_term_len(const_folding(sya(string),False))[0]))]


class Polynomial:
	def __init__(self,poly_str='NaN',degree=-1,lcoefs=[]):
		if poly_str=='NaN':
			if len(lcoefs)==0 or len(lcoefs)!=degree+1:
				self.coefs=prgm_lib.get_poly(degree)
			else:
				self.coefs=lcoefs
		else:
			self.coefs=self.str2coefs(poly_str)
		self.degree=len(self.coefs)-1
		self.numterms=len(self.coefs)
	def __call__(self,x):
		vals=[float(x)**a for a in range(self.numterms)]
		return sum(a*b for a,b in zip(self.coefs,vals))
	def __len__(self):
		return len(self.coefs)
	def degree(self):
		return len(self)-1
	def __lt__(self, other):
		if len(self)-1<other:
			return True
		else:
			return False
	def __le__(self, other):
		if len(self)-1<=other:
			return True
		else:
			return False
	def __eq__(self, other):
		if len(self)-1==other:
			return True
		else:
			return False
	def __ne__(self, other):
		if len(self)-1!=other:
			return True
		else:
			return False
	def __gt__(self, other):
		if len(self)-1>other:
			return True
		else:
			return False
	def __ge__(self, other):
		if len(self)-1>=other:
			return True
		else:
			return False
	def __getitem__(self,a):
		if type(a) is int:
			if a>=0 and a<=self.degree:
				return self.coefs[a]
			elif (a<0) and ((self.numterms+a)>=0):
				return self.coefs[self.numterms+a]
			else:
				raise IndexError
		else:
			raise TypeError
	def __setitem__(self,a,c):
		if type(a) is int:
			if a>=0 and a<=self.degree:
				self.coefs[a]=c
			elif (a<0) and ((self.numterms+a)>=0):
				self.coefs[self.numterms+a]=c
			else:
				raise IndexError
		else:
			raise TypeError
	def __contains__(self,coef):
		if coef in self.coefs:
			return True
		else:
			return False
	def __repr__(self):
		return self.coefs2str(self.coefs)
	def __str__(self):
		return self.coefs2str(self.coefs)
	def __add__(self,other):
		if type(self)==type(other):
			new=Polynomial('0')
			new.extend(max(len(self),len(other)))
			for k in range(len(new)):
				if k<len(self) and k<len(other):
					new[k] = self[k] + other[k]
				elif k<len(self):
					new[k] = self[k]
				elif k<len(other):
					new[k] = other[k]
			return new
		elif (type(other) is int) or (type(other) is float):
			new=Polynomial(str(self))
			new[0]=new[0]+other
			return new
			
	def str2coefs(self,string):
		output=sya(string)
		answer=const_folding(output,False)
		termlens=get_term_len(answer[0])
		termlens.append(0)
		slices=[int(x) for x in reversed(termlens)]
		ans=unzip(answer)
		terms=[ans[slices[k-1]:slices[k]] for k in range(1,len(slices))]
		coefs=[]
		for k in terms:
			if k[-1]=='-':
				coefs.append(float(eval('-1*'+str(k[0]))))
			else:
				coefs.append(float(k[0]))
		return coefs
	def coefs2str(self,coefs):
		string=''
		if len(coefs)==1:
			string=str(coefs[0])
		elif len(coefs)==2:
			string=str(coefs[0]) + ' + ' + str(coefs[1]) + '*x'
		elif len(coefs)>2:
			string=str(coefs[0])
			string=string + ' + ' + str(coefs[1]) + '*x'
			for k in range(2,len(coefs)):
				string = string + ' + ' + str(coefs[k]) + '*x**' + str(k)
		string=re.sub('[+][ ][-]','- ',string,re.I)
		return string
	def extend(self,n_d,val=0):
		while (len(self.coefs)<n_d+1):
			self.coefs.append(val)
		self.degree=len(self.coefs)-1
		self.numterms=self.degree+1
		

def polydiv(numc,denc):
	numt=len(numc)
	dent=len(denc)
	ansc=[]
	for a in range(numt-dent+1):
		ansc.append(float(numc[a])/float(denc[0]))
		for b in range(1,dent):
			q=a+b
			x=ansc[a]*denc[b]
			numc[q]=numc[q]-x
	rem=[]
	for c in range(numt-dent+1,numt):
		rem.append(numc[c])
	return [ansc,rem]

def ncr(n,k):
	if k>=n:
		return 1
	elif k<=0:
		return 1
	else:
		return math.factorial(n)/math.factorial(n-k)/math.factorial(k)

def factor(num):
	o_num=num
	factors=[]
	while num >=1:
		dim=len(factors)
		bound=int(math.sqrt(num))+1
		x=2
		while x<=bound:
			div=num % x
			if div == 0:
				factors.append(x)
				num=num/x
				x=bound+1
			x=x+1
		dim2=len(factors)
		if dim==dim2:
			factors.append(int(num))
			num=0
	empty=[]
	if factors==empty:
		factors.append(num)
#	print factors
	if factors[-1]==1 and o_num!=1:
		factors=factors[:-1]
	return factors


def op_preced(op):
	return op_preced_d[str(op)]
def op_left_assoc(op):
	return op_left_assoc_d[str(op)]
def op_arg_count(op):
	if op in op_list:
		return op_arg_count_d[str(op)]
	else:
		return c - 'A'
def is_operator(op):
	if op in op_list:
		return True
	else:
		return False
def is_function(op):
	if (op>='A' and op<='Z'):
		return True
	else:
		return False
def is_var(op):
	for k in str(op):
		if k in 'abcdefghijklmnopqrstuvwxyz':
			return True
	return False
### original copy of unzip() and unzip2(), moved to prgm_lib.py ###
#def unzip(lst):
#	string=unzip2(lst)
#	new_lst=re.split('_SEP_',string)
#	return new_lst[:-1]
#def unzip2(lst):
#	string=''
#	for k in lst:
#		if type(k) is list:
#			string=string+unzip2(k)
#		else:
#			string=string+str(k)+'_SEP_'
#	return string
def is_ident(op):
	if (op >= '0' and op <= 'zz') and (not is_function(op)) and (not is_operator(op)) and (not is_seperator(op)):
		return True
	else:
		return False
def is_seperator(op):
	if op==',' or op==';':
		return True
	else:
		return False

def format_input(string,long_names=False):
	string=re.sub(' ', '', string)
	string=re.sub('[*][*]', '^', string)
	string=re.sub('[+][-]', '-', string)
	t_list=[str(x) for x in string]
	string2=''
	last=''
	for x in t_list:
		if(is_ident(x)) or (is_ident(last) and x=='.'):
			string2=string2+x
		else:
			string2=string2 + ' ' + x + ' '
		last=x
	string2=string2.strip(' ')
	string2=re.sub('  ', ' ', string2)
	out_list=re.split(' ', string2)
	if out_list[0]=='-':
		out_list.insert(0,'0')
#	print out_list
	return out_list

def sya(infix_expr, long_names=False):
	token_list=format_input(infix_expr,long_names)
	output=[]
	stack=[]		
	for c in token_list:
		if(is_ident(c)):
			output.append(c)
		elif(is_function(c)):
			stack.append(c)
		elif(is_seperator(c)):
			pe=False
			while(len(stack) > 0):
				sc=stack[-1]
				if (sc == '('):
					pe=True
					break
				else:
					output.append(stack.pop())
			if not pe:
				print 'Error: seperator or parentheses mismatched'
				return False
		elif(is_operator(c)):
			while (len(stack) > 0):
				sc=stack[-1]
				if(is_operator(sc) and ((op_left_assoc(c) and (op_preced(c) <= op_preced(sc))) or (op_preced(c) < op_preced(sc)))):
					output.append(stack.pop())
				else:
					break
			stack.append(c)
		elif(c=='('):
			stack.append(c)
		elif(c==')'):
			pe=False
			while(len(stack) > 0):
				sc=stack[-1]
				if(sc=='('):
					pe=True
					break
				else:
					output.append(stack.pop())
			if not pe:
				print 'Error: parentheses mismatched'
				return False
			stack.pop()
			if(len(stack) > 0):
				sc=stack[-1]
				if(is_function(sc)):
					output.append(stack.pop())
		else:
			print 'Error, Unknown token',c
			return False
#		print output
#		print stack
#		print
	while(len(stack) > 0):
		sc=stack[-1]
		if(sc== '(' or sc==')'):
			print 'Error: parentheses mismatched'
			return False
		output.append(stack.pop())
	return output

def const_folding(rpn_list,unzipped=True,arg_counts=op_arg_count_d):
	answer=[]
	for k in rpn_list:
		temp_s=[]
		if(is_ident(k)):
			answer.append(str(k))
		elif(is_operator(k)):	
			num=arg_counts[str(k)]
			for i in range(num):
				temp_s.insert(0,answer.pop())
			temp_s.append(k)
			passes=True
			for elem in temp_s:
				if is_var(elem):
					passes=False
			if passes==True:
				if k=='^':
					out=math.pow(temp_s[0],temp_s[1])
				else:
					out=rpn_eval(temp_s)
				answer.append(out)
			else:
				answer.append(temp_s)
		elif(is_function(k)):
			if k not in arg_counts:
				print 'Error: function takes unknown amount of arguments'
				return False
			else:
				num=arg_counts[str(k)]
			for i in range(num):
				temp_s.insert(0,answer.pop())
			passes=True
			for elem in temp_s:
				if is_var(elem):
					passes=False
			temp_s.append(k)
			if passes==True:
				out=rpn_eval(temp_s)
				answer.append(out)
			else:
				answer.append(temp_s)
		else:
			print 'Error, Unknown token',k
			return False
#	print answer[0]
	if unzipped==True:
		return unzip(answer)
	else:
		return answer

def rpn_eval(rpn_expr,arg_counts=op_arg_count_d):
	string=''
	op=rpn_expr[-1]
	if is_operator(op):
		string=string+str(op)
		string=string+str(float(rpn_expr[-2]))
		if len(rpn_expr)==3:
			string=str(float(rpn_expr[0]))+string
		answer=eval(string)
	elif is_function(op):
		string=op+'('
		rpn_expr.pop()
		for k in rpn_expr:
			string=string+str(float(k)) + ','
		string=string.rstrip(',')
		string=string+')'
		answer=eval(string)
	return answer
