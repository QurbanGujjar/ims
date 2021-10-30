# from PIL import Image

# def convertImage():
# 	img = Image.open("images/icons/category.PNG")
# 	img = img.convert("RGBA")

# 	datas = img.getdata()

# 	newData = []

# 	for item in datas:
# 		if item[0] == 255 and item[1] == 255 and item[2] == 255:
# 			newData.append((255, 255, 255, 0))
# 		else:
# 			newData.append(item)

# 	img.putdata(newData)
# 	img.save("images/icons/c1.png", "PNG")
# 	print("Successful")

# convertImage()



from PIL import Image

img = Image.open('category.PNG')
img = img.convert("RGBA")
datas = img.getdata()

newData = []
for item in datas:
    if item[0] == 255 and item[1] == 255 and item[2] == 255:
        newData.append((255, 255, 255, 0))
    else:
        if item[0] > 150:
            newData.append((0, 0, 0, 255))
        else:
            newData.append(item)
            print(item)


img.putdata(newData)
img.save("c01.png", "PNG")