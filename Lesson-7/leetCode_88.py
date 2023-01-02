import copy

nums1 = [1,2,3,0,0,0]
m = 3
nums2 = [2,5,6]
n = 3

def merge_arrays(nums1,nums2,m,n):
    nums_temp = []
    j = 0
    i = 0
    cnt = 0
    while cnt !=len(nums1):
        cnt+=1
        if len(nums2)==0 or nums1[i] <= nums2[j] and nums1[i]!=0:
            nums_temp.append(nums1[i])
            i+=1
        else:
            nums_temp.append(nums2[j])
            j+=1
            if nums1[i]==0:
                i+=1

        print(nums_temp)

    return nums_temp

def merge_arrays_2(nums1,nums2,m,n):
    t=[]
    t = copy.deepcopy(nums1[:m])
    t.extend(nums2)
    t.sort()
    return t

# nums1 = [1]
# m=1
# nums2 = []
# n=0
# print(merge_arrays(nums1,nums2,m,n))



# print(t)