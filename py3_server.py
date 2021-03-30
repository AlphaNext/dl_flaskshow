from flask import Flask, request, Response, jsonify, make_response
import torch
from torch.autograd import Variable
import json
import numpy as np

import cv2
import time
import os
import base64
#os.environ['CUDA_VISIBLE_DEVICES'] = str('0')
app = Flask(__name__)
import trttools   # replace to your model inference class
import logging
logging.basicConfig(filename='detect.log',level=logging.DEBUG)

model_name = 'sim.onnx'  # final model for trt 
# define a global class for your model
trt_model = trttools.tensorrtTools(model_name, fp16_mode=True)

logging.info('model {} is used for inference!'.format(model_name))

@app.route('/api/test', methods=['POST'])
def test():
    if request.method == 'POST':
        r = request.json
        img_bytes = request.data
        image_array1 = np.frombuffer(img_bytes, dtype=np.uint8)
        img_decode = cv2.imdecode(image_array1, 1)
        #np.save('debug', img_decode)
        start = time.time()
        ### your model processinig part
        preds = trt_model.tensorrt_infer(img_decode, 1)
        end = time.time()
        ### your model processinig part
        logging.info('infernce with trt python: model input size: HxW ({} x {}), {:.4f} ms'.format(img_decode.shape[0], img_decode.shape[1], 1000*(end-start) ) )
        print('infernce with trt python {:.4f} ms'.format(1000*(end-start) ) ) 
        
        #shape = preds.shape
        # save your tensor result to json and return 
        ## response
        response = {
            'message': 'The shape is {}'.format(preds.shape),
            'map0': preds[0,0,:,:].tolist(),
            'map1': preds[0,1,:,:].tolist(),
            'map2': preds[0,2,:,:].tolist(),
            #'map0': str(preds[0,0,:,:].tobytes(), encoding='utf-8'),
            #'map1': str(preds[0,1,:,:].tobytes(), encoding='utf-8'),
            #'map2': str(preds[0,2,:,:].tobytes(), encoding='utf-8'),
            'height': preds.shape[2],
            'width': preds.shape[3]
        }
        #with open("hmm.json", 'w', encoding='utf-8') as json_file:
        #    json.dump(response, json_file, ensure_ascii=False)
        return jsonify(response)
        ## encode response using jsonpickle
        ##response_pickled = json.dumps(response)
        #return jsonify({'input': img_decode.shape, 'result': response})
        ##return Response(response=response_pickled, status=200, mimetype="application/json")

# start flask app
app.run(host="0.0.0.0", port=5770)
