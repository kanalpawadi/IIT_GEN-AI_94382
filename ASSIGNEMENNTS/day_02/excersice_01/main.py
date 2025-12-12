import math_utils
try:
    radius=float(input("enter radius for circle area : "))
    math_utils.area_of_circle(radius)
    side=float(input("enter side for square area : "))
    math_utils.area_of_sqaure(side)
    length=float(input("enter length for rectangle area : "))
    breadth=float(input("enter breadth for rectangle area : "))
    math_utils.area_of_rectangle(length,breadth)
    base=float(input("enter base for triangle area : "))
    height=float(input("enter height for triangle area : "))
    math_utils.area_of_triangle(base,height)
except :
    print("error is occured  : ")