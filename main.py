from pathlib import Path, PureWindowsPath
from tkinter import filedialog
from bs4 import BeautifulSoup
from tkinter import ttk
import tkinter as tk
import numpy as np
import shutil
import time
import glob
import os

from pathlib import Path
import configparser


class APP(tk.Tk):

    def __init__(self):
        # create X-ray folder strings
        self.xray_source_folder = ""
        self.xray_destination_folder = ""

        # get previous X-ray folders from ini file
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')  # path of .ini file
        self.xray_source_folder = self.config.get("Settings", "xray_source_folder")
        self.xray_destination_folder = self.config.get("Settings", "xray_destination_folder")

        # setup tk
        super().__init__()
        self.title('Login')
        # self.resizable(0, 0)
        self.title("Parse X-Ray report .htm file and rename images")
        self.geometry('1000x500+50+50')  # set tk window size

        # UI options
        paddings = {'padx': 5, 'pady': 5}
        entry_font = {'font': ('Helvetica', 11)}

        # configure the grid
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)

        # set the label and text variables
        self.source_folder = tk.StringVar()
        self.destination_folder = tk.StringVar()

        # configure label and button styles
        self.style = ttk.Style(self)
        self.style.configure('Heading.TLabel', font=('Helvetica', 12))
        self.style.configure('TLabel', font=('Helvetica', 11))  # , foreground="black", background="white")
        self.style.configure('TButton', font=('Helvetica', 11))  # relief styles: flat, sunken, raised, groove, ridge

        # heading
        heading = ttk.Label(self, text='X-ray routine source and rename destination folders', style='Heading.TLabel')
        heading.grid(column=0, row=0, columnspan=2, pady=5, sticky=tk.N)

        # select x-ray source folder button
        source_button = ttk.Button(self, text="Select X-ray source folder", command=self.press_source, style='TButton')
        source_button.grid(column=0, row=1, sticky=tk.W, **paddings)

        # X-ray source banner label
        source_heading = ttk.Label(self, text="X-ray source:", style='TLabel')
        source_heading.grid(column=0, row=2, sticky=tk.W, **paddings)

        # X-ray source selected location label
        source_value = ttk.Label(self, textvariable=self.source_folder, style='TLabel')
        source_value.grid(column=0, row=3, sticky=tk.W, **paddings)
        self.source_folder.set(self.xray_source_folder)

        # select renamed x-ray destination folder button
        destination_button = ttk.Button(self, text="Select X-ray destination folder", command=self.press_destination,
                                        style='TButton')
        destination_button.grid(column=0, row=4, sticky=tk.W, **paddings)

        # X-ray destination folder heading
        destination_heading = ttk.Label(self, text="X-ray destination:", style='TLabel')
        destination_heading.grid(column=0, row=5, sticky=tk.W, **paddings)

        # X-ray destination selected location label
        destination_value = ttk.Label(self, textvariable=self.destination_folder, style='TLabel')
        destination_value.grid(column=0, row=6, sticky=tk.W, **paddings)
        self.destination_folder.set(self.xray_destination_folder)

        # process X-rays
        process_button = ttk.Button(self, text="Process (rename) X-rays ", command=self.process_xrays)
        process_button.grid(column=0, row=7, sticky=tk.W, **paddings)

        # progress bar
        self.progress_bar = ttk.Progressbar(self, orient='horizontal', mode='indeterminate', length=100)
        self.progress_bar.grid(column=0, row=8, sticky=tk.W, **paddings)  # columnspan=2, padx=10, pady=20)

    # button pressed
    def press_source(self):
        self.xray_source_folder = tk.filedialog.askdirectory(title='Select X-Ray Results folder')
                                  # ,initialdir=os.path.expanduser('~') + '/Pictures/Divigraph_xrays')
        self.source_folder.set(self.xray_source_folder)
        config_file = Path('config.ini')  # Path of .ini file
        self.config.read(config_file)
        self.config.set('Settings', 'xray_source_folder', self.xray_source_folder)  # Updating existing entry
        self.config.write(config_file.open("w"))

    # button pressed
    def press_destination(self):
        self.xray_destination_folder = tk.filedialog.askdirectory(title='Select X-Ray rename folder')
                                       # ,initialdir=os.path.expanduser('~') + '/Pictures/Divigraph_xrays')
        self.destination_folder.set(self.xray_destination_folder)
        config_file = Path('config.ini')  # Path of .ini file
        self.config.read(config_file)
        self.config.set('Settings', 'xray_destination_folder', self.xray_destination_folder)  # Writing new entry
        self.config.write(config_file.open("w"))

    # button pressed
    def process_xrays(self):
        # print('\n-------------------- Start of app -------------------------------')
        print('\nxray_source_folder path:', self.xray_source_folder)
        print('\nxray_source_folder contents:', os.listdir(self.xray_source_folder))
        print('\nxray_destination_folder path:', self.xray_destination_folder)
        print('\nxray_destination_folder contents:', os.listdir(self.xray_destination_folder))

        # process
        self.progress_bar['value'] = 50
        self.update_idletasks()

        # xray_source_folder contain multiple routine folders with date code name 2022-02-02-09-56-04
        for datecode_folder in os.listdir(self.xray_source_folder):
            # routine results folder contains date code folders for each routine e.g. 2022-02-02-09-56-04
            print('folder in main xray_source_folder:', datecode_folder)
            # check if destination X-ray dump folder contains any date code folders from X-ray source folder
            if datecode_folder in os.listdir(self.xray_destination_folder):
                print(datecode_folder, "in main xray_source_folder and main dst folders")
            # check if destination X-ray dump folder does not contain a specific date code folder, copy it over
            else:
                print(datecode_folder, "not in main dst folder")
                datecode_folder_in_xray_source_folder = os.path.join(self.xray_source_folder, datecode_folder)
                print('datecode_folder_in_xray_source_folder:', datecode_folder_in_xray_source_folder)
                datecode_folder_in_xray_destination_folder = os.path.join(self.xray_destination_folder, datecode_folder)
                print('datecode_folder_in_xray_destination_folder:', datecode_folder_in_xray_destination_folder)
                shutil.copytree(datecode_folder_in_xray_source_folder, datecode_folder_in_xray_destination_folder, dirs_exist_ok=True)

                # !!! change to current datecode_folder_in_xray_destination_folder
                os.chdir(datecode_folder_in_xray_destination_folder)
                renamed_image_folder = os.path.join(datecode_folder_in_xray_destination_folder, 'renamed_image_folder')
                print('renamed_image_folder with full path: ', renamed_image_folder)

                # make rename_image_folder inside datecode_folder_in_xray_destination_folder
                if os.path.exists(renamed_image_folder):
                    shutil.rmtree(renamed_image_folder, ignore_errors=True)
                try:
                    os.makedirs(renamed_image_folder)
                except OSError:
                    print(OSError)
                finally:
                    print("os.makedirs(renamed_image_folder) successful")

                # find top .htm file
                if glob.glob('*.htm'):
                    # if routine is serialised, the file will have a name
                    htm_filename = glob.glob('*.htm')  # glob creates a list
                else:
                    # if routine is not serialised, the file will be nameless
                    htm_filename = glob.glob('.htm')  # glob creates a list
                print('htm file:', htm_filename)

                # create full outer .htm file and path, open with beautifulsoup
                # htm_full_path = os.path.join(self.xray_source_folder, htm_filename[0])  # get string from list
                # print('Outer htm file full path to parse:', htm_full_path)
                # with open(htm_full_path) as fp:
                with open(htm_filename[0]) as fp:
                    soup = BeautifulSoup(fp, 'html.parser')

                print('------ get routine name, serial number -------')
                job_elements = soup.find_all(class_="header_data")  # creates: class 'bs4.element.ResultSet'
                for job_element in job_elements:  # iterate over bs4.element.ResultSet
                    print(job_element)
                product_name = job_elements[1].string   # Divigraph_VP_CX03_v5.5.9.1_1st_side
                print('\nProduct Name:', product_name)  # will be routine name
                print('Routine serial number:', job_elements[2].string)  # will be None if no routine serial number used
                print('User:', job_elements[3].string)  # user not used on X-ray machine
                print('Run Date:', job_elements[4].string)  # run date

                print('\n------ find urls to panel sub folders ------')
                anchor_elements = soup.find_all("a")  # find all elements with <a> tags
                for anchor_element in anchor_elements:
                    print('\n ------ get inner .htm url')
                    link_url = anchor_element["href"]  # get anchor element's href attribute link destination
                    print('link_url:', link_url)
                    filename = PureWindowsPath(link_url)  # X-ray OS is Windows, use forward slashes
                    correct_path_link_url = Path(filename)
                    print('correct_path_link_url:', correct_path_link_url)
                    try:
                        print('----- open inner panel url link in beautifulsoup ------')
                        with open(correct_path_link_url) as fp:
                            soup = BeautifulSoup(fp, 'html.parser')
                            job_elements = soup.find_all(class_="header_data")
                            print('job_element type:', type(job_elements))
                            for job_element in job_elements:
                                print('job_element:', job_element, end="\n")
                            serial_nr = job_elements[2].string
                            print('Serial Number:', serial_nr)

                            print('\n--- <tr> tag from inner .htm file ---')
                            tr_tags = []
                            for tr_tag in soup.find_all('tr'):
                                if (tr_tag.get('class') == ['step_row_pass']) or (
                                        tr_tag.get('class') == ['step_row_fail']):
                                    tds_with_designator = tr_tag.find_all('td')
                                    designator = tds_with_designator[1].contents
                                    designator = designator[0]
                                    print('\ndesignator:', designator)
                                    input_tag = tds_with_designator[5].find('input')
                                    print('input_tag:', input_tag)
                                    show_image = input_tag.attrs["onclick"]  # onclick javascript function argument
                                    print('show_image:', show_image)
                                    image_name = show_image.split("\\")
                                    image_name = image_name[2].split("'")
                                    image_name = image_name[0]
                                    print('image_name: ', image_name)

                                    image_name_url = os.path.join(serial_nr, image_name)
                                    print('image_name_url: ', image_name_url)

                                    print('current directory', os.getcwd())
                                    # image from e.g. W21476-185\1_1_1.jpg to rename_image_folder
                                    try:
                                        shutil.copy(image_name_url, renamed_image_folder)
                                    except OSError:
                                        print(OSError)
                                    finally:
                                        print("shutil.copy(image_name_url, renamed_image_folder) successful")

                                    dst_file = os.path.join(renamed_image_folder, image_name)
                                    print('dst_file: ', dst_file)

                                    image_name_split = image_name.split('_')
                                    print('image_name_split: ', image_name_split)
                                    board_nr = image_name_split[1]
                                    print('board_nr: ', board_nr)

                                    serial_number_split = serial_nr.split('-')
                                    print('serial_number_split: ', serial_number_split)
                                    date_code = serial_number_split[0]
                                    print('date_code: ', date_code)
                                    panel_serial_nr = serial_number_split[1]
                                    print('panel_serial_nr: ', serial_number_split[1])

                                    product_name_split = product_name.split('_')
                                    print('product_name_split: ', product_name_split)
                                    customer = product_name_split[0]
                                    print('customer: ', customer)
                                    product = product_name_split[1] + "_" + product_name_split[2]
                                    print('product: ', product)
                                    version = product_name_split[3]
                                    print('version: ', version)

                                    # new_image_filename = customer + '_' + product_name + '_' + date_code + '-' + \
                                    new_image_filename = customer +'_'+ product +'_' + version +'_'+ date_code + '-' + \
                                                         panel_serial_nr + '-' + board_nr + '_' + designator + '_' + datecode_folder + '.jpg'
                                    # + '_' + designator + '_' + _1st_2nd + '_' + side + '.jpg'

                                    print('new_image_filename:', new_image_filename)

                                    dst_file_image_rename = os.path.join(renamed_image_folder, new_image_filename)
                                    print('dst_file_image_rename:', dst_file_image_rename)

                                    os.rename(dst_file, dst_file_image_rename)

                    except OSError:
                        print("Could not open/read file:", link_url)
                        # sys.exit


def main():
    # root = tk.Tk()  # instantiate Tk root window
    app = APP()  # instantiate APP object, Tk root window
    app.mainloop()  # enter Tk root window event loop


if __name__ == '__main__':
    main()