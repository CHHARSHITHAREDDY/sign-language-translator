# from PIL import Image
# import cv2
# import pytesseract
# from textblob import TextBlob
# import webp
# import os
# import shutil
# dest="/home/aniket/Desktop/Projects/gif_extract/gif_data/"
# op_dest="/home/aniket/Desktop/Projects/gif_extract/filtered_data/"
# for i in range(107):
#     ip=dest+str(i)+".webp"
#     op=dest+"tmp.gif"
#     anim = webp.load_images(ip)
#     anim[0].save(op, save_all=True, append_images=anim[0:1], duration=1, loop=0)
#     im = Image.open(op)
#     im.seek(0)
#     im.save("tmp.png")
#     img=cv2.imread("tmp.png")
#     try:
#         crop_img = img[0:170,200:470]
#         txt = pytesseract.image_to_string(crop_img)
#     except:
#         txt=""
#     word=txt.replace("\n", "")
#     word=word.replace(" ", "")
#     word = ''.join(filter(str.isalnum, word))
#     word=word.lower()
#     b = TextBlob(word)
#     ans=str(b.correct())
#     print("corrected text: "+ans)
#     if(len(ans)>0):
#         fname=op_dest+ans+".webp"
#         shutil.copyfile(ip, fname)
#     else:
#         fname=op_dest+"unknown"+str(i)+".webp"
#         shutil.copyfile(ip, fname)
from PIL import Image
import cv2
import pytesseract
from textblob import TextBlob
import webp
import os
import shutil

# Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\harsh\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

# Folder paths
dest = "./filtered_data/"             # Where original .webp files are
op_dest = "./filtered_data_fixed/"    # Where corrected files will go
alpha_dest = "./alphabet/"            # Letter GIFs (for other parts of the app)

# Make sure output folder exists
if not os.path.exists(op_dest):
    os.makedirs(op_dest)


for i in range(107):  # Adjust this number if needed
    ip = os.path.join(dest, f"{i}.webp")
    op = os.path.join(dest, "tmp.gif")

    try:
        anim = webp.load_images(ip)
        anim[0].save(op, save_all=True, append_images=anim[0:1], duration=1, loop=0)

        im = Image.open(op)
        im.seek(0)
        im.save("tmp.png")

        img = cv2.imread("tmp.png")
        crop_img = img[0:170, 200:470]

        txt = pytesseract.image_to_string(crop_img)
        word = txt.replace("\n", "").replace(" ", "")
        word = ''.join(filter(str.isalnum, word)).lower()

        corrected = str(TextBlob(word).correct())
        print("Corrected text:", corrected)

        if corrected:
            shutil.copyfile(ip, os.path.join(op_dest, f"{corrected}.webp"))
        else:
            shutil.copyfile(ip, os.path.join(op_dest, f"unknown{i}.webp"))

    except Exception as e:
        print(f"Error processing {ip}: {e}")
