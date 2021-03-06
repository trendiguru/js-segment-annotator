__author__ = 'jeremy'
import os
import logging
logging.basicConfig(level=logging.DEBUG)
import json
import cv2
import numpy as np
import os

from trendi import kassper
from trendi import constants


def gen_json(images_dir='data/pd_output',annotations_dir='data/pd_output',
             outfile = 'data/pd_output.json',labels=constants.pixlevel_categories_v4_for_web,mask_suffix='_pixv4_webtool.png',
             ignore_finished=True,finished_mask_suffix='_pixv4_webtool_finished_mask.png'):

    images = [os.path.join(images_dir,f) for f in os.listdir(images_dir) if '.jpg' in f and not 'legend' in f]
    the_dict = {'labels': labels, 'imageURLs':[], 'annotationURLs':[]}

    for f in images:
        print('looking at '+f)
        annotation_file = os.path.basename(f).replace('.jpg',mask_suffix)
        annotation_file = os.path.join(annotations_dir,annotation_file)
        if ignore_finished:
            maskname = annotation_file.replace(mask_suffix,finished_mask_suffix)

            #print('finished maskname:'+maskname)
            if os.path.isfile(maskname):
                print('mask '+maskname+' exists, skipping')
                continue
        if not os.path.isfile(annotation_file):
            print('could not find '+str(annotation_file))
            continue
        the_dict['imageURLs'].append(f)
        the_dict['annotationURLs'].append(annotation_file)
        print('added image '+f+' mask '+annotation_file)
    with open(outfile,'w') as fp:
        json.dump(the_dict,fp,indent=4)



def convert_pdoutput_to_webtool(dir,suffix_to_convert='.bmp',suffix_to_convert_to='.png'):
    '''
    images saved as .bmp seem to have a single grayscale channel, and an alpha.
    using 'convert' to convert those to .png doesn't help, same story. the web tool example images have the red channel
    as index, so this func converts to that format. actually i will try r=g=b=index, hopefully thats ok too - since that
    will be compatible with rest of our stuff...that didnt work , the tool really wants R=category, B=G=0
    '''
    files_to_convert=[os.path.join(dir,f) for f in os.listdir(dir) if suffix_to_convert in f]
    print(str(len(files_to_convert))+' files in '+dir)
    for f in files_to_convert:
        img_arr = cv2.imread(f)
        print('shape '+str(img_arr.shape)+ ' uniques:'+str(np.unique(img_arr)))
        h,w = img_arr.shape[0:2]
        out_arr = np.zeros((h,w,3))
        out_arr[:,:,0] = 0  #B it would seem this can be replaced by out_arr[:,:,:]=img_arr, maybe :: is used here
        out_arr[:,:,1] = 0  #G
        out_arr[:,:,2] = img_arr[:,:,0]  #R

        newname = os.path.join(dir,os.path.basename(f).replace(suffix_to_convert,suffix_to_convert_to))
        print('outname '+str(newname))
        cv2.imwrite(newname,out_arr)

        return out_arr

def skin_dir(dir):
    files = [os.path.join(dir,f)  for f in os.listdir(dir)]
    for f in files:
        img_arr=cv2.imread(f)
        mask=kassper.skin_detection(img_arr)
        mask=mask*255
        uniques = np.unique(mask)
        print uniques
        cv2.imshow('mask',mask)
        cv2.imshow('img',img_arr)
        cv2.waitKey(0)

def generate_empty_masks(dir,suffix='_pixv4_webtool.png'):
    files = [os.path.join(dir,f)  for f in os.listdir(dir)]
    for f in files:
        print('working on '+f)
        img_arr=cv2.imread(f)
        mask = np.zeros_like(img_arr)
        maskname = os.path.basename(f).replace('.jpg',suffix)
        maskname = os.path.join(dir,maskname)
        cv2.imwrite(maskname,mask)


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