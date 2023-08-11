import glob
import cv2
from natsort import natsorted

make_date = '20230802'
filepath = './image/' + make_date + '/'
imagelist = natsorted(glob.glob(filepath + '*.png'))

#print(imagelist)

#out = cv2.VideoWriter(make_date + '.mp4', cv2.VideoWriter_fourcc('m','p','4','v'), 14, (1980, 1080))
#out = cv2.VideoWriter(make_date + '.mp4', cv2.VideoWriter_fourcc('M','P','4','V'), 14, (1980, 1080))
out1 = cv2.VideoWriter(make_date + '.mp4', cv2.VideoWriter_fourcc('m','p','4','v'), 14, (2560, 1440))
out2 = cv2.VideoWriter(make_date + '-s.mp4', cv2.VideoWriter_fourcc('m','p','4','v'), 24, (2560, 1440))

for f in imagelist:
  frame = cv2.imread(f)
  
  out1.write(frame)
  out2.write(frame)

out1.release()
out2.release()
