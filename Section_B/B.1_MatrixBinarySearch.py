l=input().split() # this contains m,n as strings.
l[0],l[1]=int(l[0]),int(l[1])
k=input() # this is the element to be found.
M=[] #this is going to be the matrix, but as a one row list.

for i in range(l[0]):
    M.extend(input().split())
    
    #I'm extending rather than appending, because I'm too lazy to implement
    #binary search specifically for a matrix.
    #( It would be a crime to not binary search since we have a sorted matrix.)

def binarysearch(l,k,start=0):
    
    #Im keeping track of the start index so that I'll have the correct index being returned.
    n=len(l)
    mid=n//2
    if not n: #If the list is empty, it's not there. Job done.
        return None # Im using None rather than False since Zero is a valid index, and it might screw us over.
        
    if k==l[mid]: # Jackpot.
        return start+mid   
    elif k>l[mid]: #Search in right half 
        return binarysearch(l[mid+1:],k,start+mid+1) 
    else: #Search in left half
        return binarysearch(l[:mid],k,start)
        
      
ans=binarysearch(M,k)
if ans==None:
    print("False")
else:
    print("True")
    print(ans//l[1],ans%l[1])

