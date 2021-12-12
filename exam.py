#
# def binsearch(lst,num):
#     if len(lst) == 1 and lst[0]!=num:
#         return None
#     if lst[int(len(lst)/2)]<num:
#         res = binsearch(lst[int(len(lst)/2) + 1: len(lst)], num)
#         if not res:
#             return None
#         else:
#             return int(len(lst)/2) + res
#     if lst[int(len(lst)/2)] > num:
#         res= binsearch(lst[0: int(len(lst)/2)], num)
#         if not res:
#             return None
#         else:
#             return res
#     return 1;
#
# # lst = [2, 3,5 ,7,11,13,17,19,23,29]
# # print(binsearch(lst, 17))
#
#
#
# #Ex 2
# def minimal_sets(set_lst):
#     res= []
#     for i in set_lst:
#         flag = True
#         for j in set_lst:
#             if len(j)>= len(i):
#                 continue
#             else:
#                 count = 0
#                 for x in j:
#                     if x in i:
#                         count +=1
#                 if count == len(j):
#                     flag = False
#
#         if flag:
#             res.append(i)
#     return res
#
# lst= [{1}, {1,2}, {1,2,3},{2,4},{1}]
# print(minimal_sets(lst))
#
#
# #Ex 3,1
# def get_pairs(lst, x):
#     return  [(i, colour.index(x)) for i, colour in enumerate(lst) if x in colour]
#
# lst= [[1,2,3],[3,4,5],[3,1]]
# print(get_pairs(lst, 1))
#
# #Ex 3,2
#  def list_to_dict(lst):
#     newlst = (set(lst))
#     return dict(zip(newlst), get_pairs(list,newlst)))
#
# #print(list_to_dict(lst))
# #print(lst.index(x))
#
# import copy
# # l= [[1,2,3],[4,5,6]]
# # m=copy.deepcopy(l)
# # print(str(m[0]==l[0]) ,end=', ')
# # print(str(m[0] is l[0]))
#
#
# #Ex 4,1
# def has_driver(car, name):
#     try:
#         car.add_driver(name)
#         car.remove_driver(name)
#         return False
#     except:
#         return True
#
# #Ex 4,2
# class CarFleets:
#     def __init__(self, cars, drivers):
#         for c in cars:
#             flag= False
#             for d in drivers:
#                 if has_driver(c,d):
#                     flag=True
#             if not flag:
#                 raise Exception("Car number {} has no Driver".format(c))
#         __cars=copy.deepcopy(cars)
#         __drivers=copy.deepcopy(drivers)