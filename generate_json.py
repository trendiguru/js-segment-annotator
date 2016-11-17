__author__ = 'jeremy'
import os
import logging
import json
import cv2
import numpy as np


from trendi import constants

logging.basicConfig(level=logging.DEBUG)

def gen_json(images_dir='data/pd_output',annotations_dir='data/pd_output',outfile = 'data/pd_output.json',labels=constants.fashionista_categories):
    images = [os.path.join(images_dir,f) for f in os.listdir(images_dir) if '.jpg' in f]
    the_dict = {'labels': labels, 'imageURLs':[], 'annotationURLs':[]}

    for f in images:
        annotation_file = os.path.basename(f).replace('.jpg','.bmp')
        annotation_file = os.path.join(annotations_dir,annotation_file)
        if not os.path.isfile(annotation_file):
            logging.info('could not find '+str(annotation_file))
            continue
        the_dict['imageURLs'].append(f)
        the_dict['annotationURLs'].append(annotation_file)
    with open(outfile,'w') as fp:
        json.dump(the_dict,fp,indent=4)


def convert_pdoutput_to_webtool(dir,suffix_to_convert='.bmp',suffix_to_convert_to='.png'):
    '''
    images saved as .bmp seem to have a single grayscale channel, and an alpha.
using 'convert' to convert those to .png doesn't help, same story. the web tool example images have the red channel
 as index, so this func converts to that format. actually i will try r=g=b=index, hopefully thats ok too - since that
 will be compatible with rest of our stuff
    '''
    files_to_convert=[os.path.join(dir,f) for f in os.listdir(dir) if suffix_to_convert in f]
    for f in files_to_convert:
        img_arr = cv2.imread(f)
        print('shape '+str(img_arr.shape)+ ' uniques:'+str(np.unique(img_arr)))
        h,w = img_arr.shape[0:2]
        out_arr = np.zeros((h,w,3))
        out_arr[:,:,0] = img_arr[:,:,0]  #it would seem this can be replaced by out_arr[:,:,:]=img_arr, maybe :: is used here
        out_arr[:,:,1] = img_arr[:,:,0]
        out_arr[:,:,2] = img_arr[:,:,0]
        newname = os.path.join(dir,os.path.basename(f).replace(suffix_to_convert,suffix_to_convert_to))
        print('outname '+str(newname))
        cv2.imwrite(newname,out_arr)

if __name__ == "__main__":
    gen_json()


'''
{
  "labels": [
    "background",
    "skin",
    "hair",
    "dress",
    "glasses",
    "jacket",
    "skirt"
  ],
  "imageURLs": [
    "data/images/1.jpg",
    "data/images/2.jpg"
  ],
  "annotationURLs": [
    "data/annotations/1.png",
    "data/annotations/2.png"
  ]
}

'''