import glob
import cv2
from natsort import natsorted

make_date = '20221203'
filepath = './image/' + make_date + '/afmhot/'
imagelist = natsorted(glob.glob(filepath + '*.png'))

#print(imagelist)

out = cv2.VideoWriter(make_date + '_afmhot.mp4', cv2.VideoWriter_fourcc('M','P','4','V'), 7, (1980, 1080))
#out = cv2.VideoWriter(make_date + '.mp4', cv2.VideoWriter_fourcc('M','P','4','V'), 14, (1980, 1080))
#out = cv2.VideoWriter(make_date + '.mp4', cv2.VideoWriter_fourcc('M','P','4','V'), 24, (2560, 1440))

for f in imagelist:
  frame = cv2.imread(f)
  
  out.write(frame)

out.release()