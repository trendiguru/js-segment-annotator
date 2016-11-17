__author__ = 'jeremy'
import os
import logging
import json

logging.basicConfig(level=logging.DEBUG)

fashionista_categories = ['background','tights','shorts','blazer','t-shirt','bag','shoes','coat','skirt','purse',
                                    'boots','blouse','jacket','bra','dress','pants','sweater','shirt','jeans','leggings',
                                    'scarf','hat','top','cardigan','accessories','vest','sunglasses','belt','socks','glasses',
                                    'intimate','stockings','necklace','cape','jumper','sweatshirt','suit','bracelet','heels','wedges',
                                    'ring','flats','tie','romper','sandals','earrings','gloves','sneakers','clogs','watch',
                                    'pumps','wallet','bodysuit','loafers','hair','skin','face']

def gen_json(images_dir='data/pd_output',annotations_dir='data/pd_output',outfile = 'data/pd_output.json',labels=fashionista_categories):
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