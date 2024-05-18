import oled 
import time
import numpy as np
from PIL import Image
matrixs = np.zeros((128,128))
last_matrixs = np.zeros((128,128))
value = 0 
x = 0
y = 0

def compare_matrices_with_areas(matrix1, matrix2):
    if matrix1.shape != (128, 128) or matrix2.shape != (128, 128):
        print("Error: Matrices must be 128x128.")
        return []

    # Initialize a list to store the coordinates of differences
    differences = []

    # Iterate through each area of the matrices (16 areas per row, 16 columns)
    for row_area in range(16):
        for col_area in range(16):
            area_start_row = row_area * 8 
            area_end_row = (row_area + 1) * 8
            area_start_col = col_area * 8
            area_end_col = (col_area + 1) * 8

            # Check if the area in both matrices is the same
            area_diff = False
            for i in range(area_start_row, area_end_row):
                for j in range(area_start_col, area_end_col):
                    if matrix1[i, j] != matrix2[i, j]:
                        area_diff = True
                        break
                if area_diff:
                    break

            # If the area is different, add it to the list of differences
            if area_diff:
                differences.append((row_area, col_area))

    return differences

def pixel(matrix,x,y,state):
    matrix[x,y] = state

def convert(i,s,matrix): 
    x = i[0]
    y = i[1]
    location =  x * 8 + s #location of current line in matrix
    output_array = []
    for pixel in range(8):
        y_info = matrix[location,pixel + y * 8]
        output_array.insert(0,int(y_info))
    output_string =  ''.join(str(bit) for bit in output_array)
    output_number = int(output_string, 2)
    return output_number

def oled_update(i,a,matrix):
    a.setCursor(i[1],i[0])
    for s in range(8):
        line = convert(i,s,matrix)
        a._datas([line])
def frame(a,matrix,last_matrix):
    diff = compare_matrices_with_areas(matrix,last_matrix)
    for i in diff:
        oled_update(i,a,matrix)
    last_matrix[:, :] = matrix

def rect(x,y,width,height,n,matrix):
    for i in range(x, x + width):
        for j in range(y, y + height):
            pixel(matrix,i, j, n)


def line(x1, y1, x2, y2, n,matrix):
    # Check if the points are within the bounds of the matrix
    if x1 < 0 or x1 >= matrix.shape[0] or y1 < 0 or y1 >= matrix.shape[1] or \
       x2 < 0 or x2 >= matrix.shape[0] or y2 < 0 or y2 >= matrix.shape[1]:
        print("Error: Points are outside the bounds of the matrix.")
        return

    # Calculate the differences and absolute differences between the points
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy

    # Loop through the points and draw the line
    while True:
        # Set the pixel at (x1, y1) to the specified value
        matrix[x1, y1] = n

        # Check if we've reached the end point
        if x1 == x2 and y1 == y2:
            break

        # Calculate the next pixel position
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy
def fullscreen_image(name, matrix):
    image = Image.open(name)
    new_matrix = np.array(image)
    new_matrix = new_matrix.astype(int)
    matrix[:, :] = new_matrix
def write(string,x,y,n,matrix):
    for i in range(len(string)):
        putchar(string[i],i,x,8*y,n,matrix)
def putchar(c,i,pre_x,y,n,matrix):
    x = i + pre_x
    asc = ord(c)
    if asc < 32 or asc > 127:
        asc = ord(' ')
    for i in range(8):
        fontmap = (oled.BasicFont[asc - 32][i])
        canva_modify(fontmap,x,y,i,n,matrix)
def canva_modify(fontmap,prex,y,i,n,matrix):
    x = prex * 8 + i
    output = int_to_8bit_binary(fontmap,n)
    for b in range(8):
        matrix[x,y+7-b] = output[b] 

def int_to_8bit_binary(num,n):
    # Convert the number to binary string representation
    binary_str = bin(num & 0xFF)
    invert_binary_str = bin(~int(binary_str, 2) & 0xFF)
    # Pad with zeros to ensure it's 8 bits long
    if n == 1:
        padded_binary_str = binary_str[2:].zfill(8)
    else:
        padded_binary_str = invert_binary_str[2:].zfill(8)
    return padded_binary_str

def scrolling_chart(t,x1, y1, x2, y2, c, matrix):
# Ensure c is between 0 and 3000
    c = max(0, min(c, t * 2))
    # Calculate the height of the bar based on c
    bar_height = int((c / (t*2)) * (y2 - y1))

    line(x2,(y2 - y1)-bar_height,x2,y2,1,matrix)

    matrix = np.roll(matrix, -1, axis=1)




if __name__ == '__main__':
    a = oled.SH1107G_SSD1327()
    a.backlight(False)
    time.sleep(1)
    a.backlight(True)
    rect(4,7,50,40,1,matrixs)
    write('aasdasd',0,0,1,matrixs)
    frame(a,matrixs,last_matrixs)
    time.sleep(2)
    write('aasdxfe',0,0,0,matrixs)
    time.sleep(2)
    frame(a,matrixs,last_matrixs)
    for i in range(6573):
        s = 'frame128/' + str(i+1) +'.bmp'
        fullscreen_image(s,matrixs)
        print(i)
        frame(a,matrixs,last_matrixs)
   # matrix1 = np.rot90(matrix)
   # matrix2 = np.rot90(matrix, k=-1)
   # time.sleep(2)
   # frame(a)
