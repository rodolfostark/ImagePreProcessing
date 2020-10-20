import cv2
import numpy as np
import threading
from time import sleep

def handleContrastEnlargement(img, height, width):
    Imax = img.max()
    Imin = img.min()
    g = np.zeros((height,width), np.uint8)
    print(g)
    for i in range(0, height):
        for j in range(0, width):
            g[i][j] = (255 // (Imax - Imin)) * (img[i][j] - Imin)
    cv2.imwrite('imageContrastEnlarged.png', g)

# Retorna o histograma da imagem I
def handleOccourenceHistogram(img, height, width):
    hist = [0] * 256
    for i in range(height):
        for j in range(width):
            hist[img[i][j]] += 1
    return hist

# Retorna a probabilidade de ocorrência de cada valor de pixel
def handleOccourenceProbability(hist, height, width):
    prob = [0] * 256
    for i in range(0, 256):
        prob[i] = hist[i] / (height * width)   
    return prob

# Retorna a probabilidade acumulada
def handleAccumulatedProbability(prob):
    prob_ac = [0] * 256
    for i in range(0, 256):
        cont = 0
        for j in range(0, i):
            cont += prob[j]
        prob_ac[i] = cont
    return prob_ac

def handleHistogramEqualization(img, height, width):
    hist = handleOccourenceHistogram(img, height, width)
    prob = handleOccourenceProbability(hist, height, width)
    prob_ac = handleAccumulatedProbability(prob)

    g = np.zeros((height,width), np.uint8)
    for i in range(height):
        for j in range(width):
            g[i][j] = round(255 *  prob_ac[img[i][j]])

    cv2.imwrite('imageEqualized.png', g)


if __name__ == '__main__':
    #lendo o arquivo
    image_path = 'balloons.png'
    image = cv2.imread(image_path, 0)
    height, width = image.shape

    primera_thread = threading.Thread(target=handleContrastEnlargement, args=(image, height, width))
    segunda_thread = threading.Thread(target=handleHistogramEqualization, args=(image, height, width))

    primera_thread.start()
    segunda_thread.start()

    primera_thread.join()
    segunda_thread.join()

    while primera_thread.is_alive():
        sleep(1)
    print('Finalizando primeira thread.')

    while segunda_thread.is_alive():
        sleep(1)
    print('Finalizando segunda thread.')
