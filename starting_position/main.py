import urllib.request as urllib2
from bs4 import BeautifulSoup
import PIL
import glob
from PIL import Image
import numpy as np
import json
import os

url = "https://abaloneonline.wordpress.com/tag/starting-positions/"


def download_image(pic_name, pic_url):

    with open(pic_name, 'wb') as f:
        r = urllib2.urlopen(pic_url)
        if r.status == 200:
            f.write(r.read())

def download():
    req = urllib2.urlopen(url)
    if req.status == 200:
    
        soup = BeautifulSoup(req, "lxml")
        imgs = soup.find('div', {'class':'entry-content'}).find_all('a')
        for img in imgs:
            pic_url = img['href']
            pic_name = f"80/{pic_url.split('/')[-1]}"

            print(pic_name)
            download_image(pic_name, pic_url)


def mse(pixel0, pixel1):
    return sum((p0-p1)**2 for p0, p1 in zip(pixel0, pixel1)) / len(pixel0) 


def detect_pixel(pixel):
    '''
    find the closest between 
        ''  : void  : (170, 146, 102)
        'w' : white : (210, 210, 210)
        'b' : black : ( 68,  68,  68)
    '''
    colors = [(170,146,102), (210,210,210), (68,68,68)]
    p_color = ['_', 'w', 'b']

    i_min = np.argmin([mse(pixel, c) for c in colors])
    return p_color[i_min]


def repr_board(out):
    '''
    #     _ _ _ _ _
    #    w w w w w w
    #   w b w _ _ _ w
    #  _ w w _ _ w w _
    # _ _ _ _ _ _ _ _ _
    #  _ b b _ _ b b _
    #   b _ _ _ b w b
    #    b b b b b b
    #     _ _ _ _ _
    '''

    tmp = [5, 6, 7, 8, 9, 8, 7, 6, 5]
    print(sum(tmp))
    i = 0
    j = 0
    for x in out:
        if i==0:
            print(' '*(9-tmp[j]), end='')
        print(x, end=' ')
        if i < tmp[j]-1:
            i += 1
        else:
            i = 0
            j += 1
            print()
    print()

def process():

    # find all the positions from red pixel in the test image 
    data = np.array(Image.open('test.png'))
    pos = []
    for row in range(data.shape[0]):
        for col in range(data.shape[1]):
            r, g, b = data[row, col, :3]
            if (r, g, b) == (255, 0, 0):
                pos.append((row, col))


    configs = []
    images = glob.glob('80/*')
    for image_id, image in enumerate(images):
        print(image)
    
        base =  os.path.basename(image)
        name = os.path.splitext(base)[0]
        data = np.array(Image.open(image))

        config = {
            'name': name,
            'id' : image_id,
            'black': [],
            'white': []
        }

        out = []
        for i, (row, col) in enumerate(pos):
            r, g, b = data[row, col, :3]
            value = detect_pixel((r,g,b))
            if value !=  '_':
                config[{'b':'black', 'w':'white'}[value]].append(i)
            out.append(value)

        try:
            assert len(config['black'])==len(config['white'])
        except AssertionError:
            repr_board(out)


        configs.append(config)


    # Writing JSON data
    with open('variants.json', 'w') as f:
        json.dump(configs, f, indent=1)


    return




    
    '''
    'I5','I6','I7','I8','I9',
    'H4','H5','H6','H7','H8','H9',
    'G3','G4','G5','G6','G7','G8','G9',
    'F2','F3','F4','F5','F6','F7','F8','F9',
    'E1','E2','E3','E4','E5','E6','E7','E8','E9',
    'D1','D2','D3','D4','D5','D6','D7','D8',
    'C1','C2','C3','C4','C5','C6','C7',
    'B1','B2','B3','B4','B5','B6',
    'A1','A2','A3','A4','A5',
    '''

if __name__ == '__main__':

     process()
