import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import os
import cv2
from signature import match

# Match Threshold
THRESHOLD = 85

def browsefunc(ent):
    filename = askopenfilename(filetypes=([
        ("image", ".jpeg"),
        ("image", ".png"),
        ("image", ".jpg"),
    ]))
    ent.delete(0, tk.END)
    ent.insert(tk.END, filename)

def capture_image_from_cam_into_temp(sign=1):
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cv2.namedWindow("test")

    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("test", frame)

        k = cv2.waitKey(1)
        if k % 256 == 27:
            print("Escape hit, closing...")
            break
        elif k % 256 == 32:
            if not os.path.isdir('temp'):
                os.mkdir('temp', mode=0o777)
            img_name = "./temp/test_img1.png" if sign == 1 else "./temp/test_img2.png"
            print('imwrite=', cv2.imwrite(filename=img_name, img=frame))
            print("{} written!".format(img_name))
    cam.release()
    cv2.destroyAllWindows()
    return True

def captureImage(ent, sign=1):
    filename = os.getcwd() + '\\temp\\test_img1.png' if sign == 1 else os.getcwd() + '\\temp\\test_img2.png'
    res = messagebox.askquestion('Click Picture', 'Press Space Bar to click picture and ESC to exit')
    if res == 'yes':
        capture_image_from_cam_into_temp(sign=sign)
        ent.delete(0, tk.END)
        ent.insert(tk.END, filename)
    return True

def checkSimilarity(window, path1, path2):
    result = match(path1=path1, path2=path2)
    if(result <= THRESHOLD):
        messagebox.showerror("Failure: Signatures Do Not Match", "Signatures are "+str(result)+f" % similar!!")
    else:
        messagebox.showinfo("Success: Signatures Match", "Signatures are "+str(result)+f" % similar!!")
    return True

root = tk.Tk()
root.title("Signature Matching")
root.geometry("500x700")

# Centering elements
frame = tk.Frame(root)
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Add heading
heading_label = tk.Label(frame, text="Compare the Signature Here", font=("Helvetica", 14, "bold"))
heading_label.pack(pady=20)

uname_label = tk.Label(frame, text="Compare Two Signatures:", font=10)
uname_label.pack(pady=10)

img1_message = tk.Label(frame, text="Signature 1", font=10)
img1_message.pack(pady=5)

image1_path_entry = tk.Entry(frame, font=10, width=40)
image1_path_entry.pack(pady=5)

img1_buttons_frame = tk.Frame(frame)
img1_buttons_frame.pack(pady=5)

img1_capture_button = tk.Button(img1_buttons_frame, text="Capture", font=10, bg="lightblue", command=lambda: captureImage(ent=image1_path_entry, sign=1))
img1_capture_button.pack(side=tk.LEFT, padx=5)

img1_browse_button = tk.Button(img1_buttons_frame, text="Browse", font=10, bg="lightgreen", command=lambda: browsefunc(ent=image1_path_entry))
img1_browse_button.pack(side=tk.LEFT, padx=5)

separator = tk.Frame(frame, height=2, bd=1, relief=tk.SUNKEN)
separator.pack(fill=tk.X, pady=20)

img2_message = tk.Label(frame, text="Signature 2", font=10)
img2_message.pack(pady=5)

image2_path_entry = tk.Entry(frame, font=10, width=40)
image2_path_entry.pack(pady=5)

img2_buttons_frame = tk.Frame(frame)
img2_buttons_frame.pack(pady=5)

img2_capture_button = tk.Button(img2_buttons_frame, text="Capture", font=10, bg="lightblue", command=lambda: captureImage(ent=image2_path_entry, sign=2))
img2_capture_button.pack(side=tk.LEFT, padx=5)

img2_browse_button = tk.Button(img2_buttons_frame, text="Browse", font=10, bg="lightgreen", command=lambda: browsefunc(ent=image2_path_entry))
img2_browse_button.pack(side=tk.LEFT, padx=5)

compare_button = tk.Button(frame, text="Compare", font=10, bg="orange", command=lambda: checkSimilarity(window=root,
                                                                                                        path1=image1_path_entry.get(),
                                                                                                        path2=image2_path_entry.get()))
compare_button.pack(pady=20)

root.mainloop()
