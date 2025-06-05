import os
import time
import sys

def lecture():
    c =  input("今天上課嗎(Y/N): ")
    if c == "Y" or c == "y":
        print("今天有課，請準時上課！")
        return True
    elif c == "N" or c == "n":
        print("今天沒有課，可以休息一下！")
        return False
    else: 
        print("請輸入正確的選項（Y/N）")
        return lecture()