import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'


import matplotlib.pyplot as plt
import numpy as np
import cv2
import tensorflow as tf


from fastapi import FastAPI, Response
from PIL import Image

import io

from sklearn.metrics import f1_score 
from keras import optimizers
from keras.models import Sequential
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import load_model

from keras.layers import Dense, Flatten, MaxPooling2D, Dropout, Conv2D



# Визначення шляхів для завантаження ресурсів
models_file_path = './src/static/'
file_model = 'model.h5'
file_cascad = 'cascad.xml'
full_path_models = os.path.join(models_file_path, file_model)  
full_path_cascad = os.path.join(models_file_path, file_cascad)

# Завантаження моделі та каскадного класифікатора
model = load_model(full_path_models)
plate_cascade = cv2.CascadeClassifier(full_path_cascad)





# Function to resize the image to a fixed height
def resize_img(img, target_height=720):
    # Get the original image's height and width
    height, width = img.shape[:2]
    # If the original image's height is less than or equal to the target height,
    # return the original image as it is
    if height <= target_height:
      return img
    # Calculate the target width by maintaining the aspect ratio
    target_width = int(width * (target_height / height))
    # Resize the image to the target width and height using OpenCV's resize function
    resized_img = cv2.resize(img, (target_width, target_height))
    
    # Return the resized image
    return resized_img


# Визначає та виконує розмиття на номерних знаках
def extract_plate(img, plate_cascade):
    
    # Copy the original image for processing
    plate_img = img.copy()
    roi = img.copy()
    plate = None
    
    # Detect license plate contours in the image
    plate_rect = plate_cascade.detectMultiScale(plate_img, scaleFactor = 1.05, minNeighbors = 8)

    # Iterate through the detected contours
    for (x,y,w,h) in plate_rect:

        # Calculate the offsets for the plate
        a, b = (int(0.1 * h), int(0.1 * w)) 
        aa, bb = (int(0.1 * h), int(0.1 * w))

        
        # Adjust the offsets if the plate height is high
        if h > 75: 
            b = 0
            bb = 0

        # Extract the plate from the ROI
        plate = roi[y+a : y+h-aa, x+b : x+w-bb, :]

    return plate_rect, plate

# Відповідність контурів номерному або символьному шаблону
def find_contours(dimensions, img):

    # Define the minimum width threshold for character contours
    i_width_threshold = 6 

    # Find contours in the image
    cntrs, _ = cv2.findContours(img.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Define the lower and upper width and height thresholds for character contours
    lower_width = dimensions[0]
    upper_width = dimensions[1]
    lower_height = dimensions[2]
    upper_height = dimensions[3]
    upper_height = dimensions[3]

    # Sort the contours by their area in descending order and limit to the first 16 contours
    cntrs = sorted(cntrs, key=cv2.contourArea, reverse=True)[:16]

    # Create a 3-channel image for drawing bounding rectangles
    ii = np.dstack([img] * 3)

    # Initialize a list to store the x-coordinates of the contours
    x_cntr_list = []

    # Initialize a list to store the cropped character images
    img_res = []

    # Iterate through each contour
    for cntr in cntrs:

        # Get the bounding rectangle of the contour
        intX, intY, intWidth, intHeight = cv2.boundingRect(cntr)

        # Check if the contour meets the width and height thresholds
        if (intWidth >= i_width_threshold and intWidth < upper_width and intHeight > lower_height and intHeight < upper_height):
            # Append the x-coordinate of the contour to the list
            x_cntr_list.append(intX)

            # Crop the character image from the original image
            char = img[intY:intY + intHeight, intX:intX + intWidth]

            # Check if the character image width is within the lower width threshold
            if (intWidth >= i_width_threshold and intWidth < lower_width):
                # Resize the character image to a fixed width and height
                i_char = cv2.resize(char, (intWidth, 42), interpolation=cv2.INTER_LINEAR_EXACT)

                # Create a new image with a white background
                char = np.full((42, 22), 255, dtype=np.uint8)

                # Calculate the starting x-coordinate for placing the resized character image
                begin = int((22 - intWidth) / 2)

                # Place the resized character image on the new image
                char[:, begin:begin + intWidth] = i_char[:, :]
            else:
                # Resize the character image to a fixed width and height
                char = cv2.resize(char, (22, 42), interpolation=cv2.INTER_LINEAR_EXACT)

            # Draw a bounding rectangle around the character image
            cv2.rectangle(ii, (intX, intY), (intWidth + intX, intY + intHeight), (50, 21, 200), 2)
            
            
            # Invert the colors of the character image
            char = cv2.subtract(255, char)

            # Set the top and bottom borders of the character image to white
            char[0:1, :] = 0
            char[:, 0:1] = 0
            # Set the left and right borders of the character image to white
            char[43:44, :] = 0
            char[:, 23:24] = 0
            # Append the cropped character image to the list
            img_res.append(char)
        # Break the loop if the number of cropped character images reaches 10
        if len(img_res) >= 10:
            break
    # Return the list of cropped character images
    return img_res


# Find characters in the resulting images
def segment_to_contours(image):

    # Set the fixed height for the license plate image
    new_height = 75 

    # Preprocess the cropped license plate image by resizing it to the fixed height
    img_lp = cv2.resize(image, (333, new_height), interpolation=cv2.INTER_LINEAR_EXACT)



    # Convert the resized image to grayscale
    img_gray_lp = cv2.cvtColor(img_lp, cv2.COLOR_BGR2GRAY)

    # Apply Otsu's binarization method to threshold the grayscale image
    _, img_binary_lp = cv2.threshold(img_gray_lp, 112, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Get the width and height of the thresholded image
    LP_WIDTH = img_binary_lp.shape[1]
    LP_HEIGHT = img_binary_lp.shape[0]

    # Make the borders of the thresholded image white
    img_binary_lp[0:3,:] = 255
    img_binary_lp[:,0:3] = 255
    img_binary_lp[new_height-3:new_height,:] = 255
    img_binary_lp[:,330:333] = 255

    # Estimate the sizes of the character contours based on the dimensions of the thresholded image
    dimensions = [LP_WIDTH/24,
                LP_WIDTH/8,
                LP_HEIGHT/3,
                2*LP_HEIGHT/3]


    # Get the character contours within the thresholded image using the estimated dimensions
    char_list = find_contours(dimensions, img_binary_lp)

    # Return the list of character contours
    return char_list

def fix_dimension(img): 
    # Create a new 3D numpy array with zeros, representing a 28x28 image with 3 color channels
    new_img = np.zeros((28,28,3))

    # Iterate through each color channel (0 for blue, 1 for green, 2 for red)
    for i in range(3):
        # Copy the original image's color channel to the corresponding position in the new image
        new_img[:,:,i] = img

    # Return the resized and reshaped image
    return new_img

# Predicting the output string number by contours
def predict_result(ch_contours, model):


    # Create a dictionary to map the model's output indices to the corresponding characters
    dic = {}
    characters = '#0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for i,c in enumerate(characters):
        dic[i] = c

    
    # Initialize an empty list to store the predicted characters
    output = []
    
    # Iterate through each character contour
    for i,ch in enumerate(ch_contours):

        # Resize the character image to a fixed size of 28x28 pixels
        img_ = cv2.resize(ch, (28,28)) 

        # Prepare the image for the model by reshaping it to a 4D tensor
        img = fix_dimension(img_)
        img = img.reshape(1, 28, 28, 3) #preparing image for the model

        # Use the model to predict the class (character) of the image
        y_ = np.argmax(model.predict(img, verbose=0), axis=-1)[0] 

        # Map the predicted class to the corresponding character using the dictionary
        character = dic[y_]

        # Append the predicted character to the output list
        output.append(character)
        

    # Join the predicted characters into a string to form the license plate number
    plate_number = ''.join(output)

    # Return the predicted license plate number
    return plate_number




def get_plate_number(img_avto):
    # Copy the original image for processing
    img = img_avto.copy()
    
    # Extract the license plate from the original image
    output_img, num_img = extract_plate(img, plate_cascade)

    
    # Segment the characters in the extracted license plate
    chars = segment_to_contours(num_img)

    # Predict the license plate number using the segmented characters
    predicted_str = predict_result(chars, model)
    
    # Replace any '#' characters in the predicted license plate number with an empty string
    num_avto_str = str.replace(predicted_str, '#', '')    

    
    
    # If the license plate was successfully extracted
    if output_img is not None:

        # Get the coordinates of the extracted license plate
        x, y, w, h = output_img[0]
        
        # Draw a bounding rectangle around the extracted license plate
        cv2.rectangle(img, (x+2,y), (x+w-3, y+h-5), (0,0,245), 3)
        
        # Add the predicted license plate number as text on the original image
        cv2.putText(img, num_avto_str, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,245), 5)

    # Convert the numpy array to an image
    img_pil = Image.fromarray(img)

    # Save the image to a file-like object
    img_io = io.BytesIO()
    img_pil.save(img_io, format='JPEG')
    
    # Return the predicted license plate number and the image as a response
    return [num_avto_str, Response(content=img_io.getvalue(), media_type="image/jpeg")]

if __name__ == '__main__':
    # Визначення шляхів для завантаження ресурсів
    models_file_path = 'your_models_path'
    file_model = 'model.h5'
    file_cascad = 'cascad.xml'
    full_path_models = os.path.join(models_file_path, file_model)  
    full_path_cascad = os.path.join(models_file_path, file_cascad)

    # Завантаження моделі та каскадного класифікатора
    model = load_model(full_path_models)
    plate_cascade = cv2.CascadeClassifier(full_path_cascad)

    img_file_path = 'your_images_path'
    file_img = '10.jpg'
    full_path_img = os.path.join(img_file_path, file_img)

    original = cv2.imread(full_path_img)
    if original is None:
        print("Помилка завантаження зображення. Перевірте шлях до файлу.")
        exit(1)


    result = get_plate_number(original)
    print(f'ok - {result}')