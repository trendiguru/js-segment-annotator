__author__ = 'jeremy'
import os
import logging
import json

logging.basicConfig(level=logging.DEBUG)

def gen_json(images_dir='./pd_output',annotations_dir='./pd_output',outfile = 'pd_output.json'):
    images = [os.path.join(images_dir,f) for f in os.listdir(images_dir)]
    the_dict = {'labels':    ["background",
    "skin",
    "hair",
    "dress",
    "glasses",
    "jacket",
    "skirt"],

    'imageURLS':[],
    'annotationURLS':[]}

    for f in images:
        annotation_file = os.path.join(annotations_dir,os.path.basename(f))
        if not os.path.isfile(annotation_file):
            logging.info('could not find '+str(annotation_file))
        the_dict['imageURLs'].append(f)
        the_dict['annotationURLs'].append(f)
    with open(outfile,'w') as fp:
        json.dump(the_dict,fp)

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