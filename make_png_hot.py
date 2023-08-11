import os
import time
import re
import requests
from bs4 import BeautifulSoup

import numpy as np
import matplotlib.pyplot as plt

import japanize_matplotlib
from astropy.io import fits
from astropy.utils.data import download_file

d_year = '2022'
d_date = '20221203'

url_base = 'https://solarwww.mtk.nao.ac.jp/mitaka_solar/ha-mtkft1/fts/'

url = url_base + d_year + '/' + d_date + '/'

r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')
get_list = soup.find_all('a')

pattern = 'mtk_ft_ha_fd_\d{8}T\d{6}_i_000_m.fts.gz'

prog = re.compile(pattern)

figsize_px = np.array([1980, 1080])
dpi = 300
figsize_inch = figsize_px / dpi

png_no = 0

filepath = './image/' + d_date + '/hot/'
os.makedirs(filepath, exist_ok=True)

for i, fits_list in enumerate(get_list):
    
    fits_href = fits_list.attrs['href']

    if prog.match(fits_href):

        png_no += 1

        # sleep
        time.sleep(1)
        print(png_no, fits_list)

        image_file = download_file(url + fits_href, cache=True )

        hdu_list = fits.open(image_file)
        
        image_header = hdu_list[0].header
        image_data = hdu_list[0].data
        
        hdu_list.close()

        image_dt_target = 'T'
        image_date_time = image_header['DATE_OBS']
        dtidx = image_date_time.find(image_dt_target)
        image_date = image_date_time[:dtidx]
        image_time = image_date_time[dtidx+len(image_dt_target):]

        image_UT_target = '.'
        UTidx = image_time.find(image_UT_target)
        image_time_UT = image_time[:UTidx] + ' UT'

        save_date = image_date[:4] + image_date[5:7] + image_date[8:]
        save_time = image_time[:2] + image_time[3:5] + image_time[6:8]

        png_no_str = str(png_no)

        fig = plt.figure(dpi=dpi, figsize=(figsize_inch), facecolor='lightgray')

        ax1 = fig.add_subplot(1, 1, 1)
        #ax2 = fig.add_subplot(1, 2, 2)
        fig.subplots_adjust(left=0.05, bottom=0.03, right=0.95, top=0.97, wspace=0.12)

        ax1.axis("off")
        #ax2.axis("off")

        ax1.text(15, 1970, image_header['OBJECT'] + ' / ' + image_header['WAVELNTH']+ ' / ' + image_header['TYPE_OBS'], color='whitesmoke', size='small')
        ax1.text(15, 15, image_date + ' ' + image_time_UT, color='whitesmoke', size='small')
        ax1.text(1550, 15, 'Courtesy of NAOJ', color='whitesmoke', size='x-small')

        #ax2.text(15, 1970, image_header['OBJECT'] + ' / ' + image_header['WAVELNTH']+ ' / ' + image_header['TYPE_OBS'] + ' / gray', color='whitesmoke', size='small')
        #ax2.text(15, 15, image_date + ' ' + image_time_UT, color='whitesmoke', size='small')
        #ax2.text(1450, 15, 'Courtesy of NAOJ', color='whitesmoke', size='x-small')

        ax1.imshow(image_data, cmap='afmhot', origin='lower')
        #ax2.imshow(image_data, cmap='gray', origin='lower')

        fig.savefig(filepath + 'im_' + png_no_str + '_' + save_date + '_' + save_time + '.png', format='png', dpi=dpi)

        plt.clf()
        plt.close()

    if png_no == 1000:
        break
