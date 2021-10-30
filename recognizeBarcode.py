import cv2
from pyzbar.pyzbar import decode
import time
# img=cv2.imread('images/MybarCode.jpeg')
# print(len(decode(img)))
cap =cv2.VideoCapture(0)
cap.set(3,340)  #3= width
cap.set(4,280)  # 4= height
used_codes=[]
try:
        
    camera =True
    while camera ==True:
        success,frame =cap.read()
        for code in decode(frame):
            if code.data.decode('utf-8') not  in used_codes:
                print('Approved.You can Enter')
                print(code.data.decode('utf-8'))
                used_codes.append(code.data.decode('utf-8'))
                time.sleep(5)
                camera =False
            elif code.data.decode('utf-8') in used_codes:
                print('Sorry it is in')
                time.sleep(5)
            else:
                pass        
            # print(code.type)
            # print(code.data.decode('utf-8'))
        cv2.imshow('Testing code scan',frame)
        cv2.waitKey(1)
except Exception as Ex:
    pass        
print("Exit")    