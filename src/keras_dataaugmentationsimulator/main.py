import argparse

import matplotlib.pyplot as plt
import numpy as np
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
from matplotlib.widgets import Button, RadioButtons, Slider
from PIL import Image


AXCOLOR = "lightgoldenrodyellow"


class WidgetSlider:
    def __init__(self, rect, name, min_val, max_val, init_val, callback_dict):
        self.axes = plt.axes(rect, facecolor=AXCOLOR)
        self.widget = Slider(self.axes, name, min_val, max_val, init_val)

        for name, func in callback_dict.items():
            self._set_callback(name, func)

    def _set_callback(self, name, func):
        if name == "on_changed":
            self.widget.on_changed(func)
        else:
            print("name not found : ", name)

    def get_val(self):
        return self.widget.val


class WidgetButton:
    def __init__(self, rect, name, callback_dict):
        self.axes = plt.axes(rect, facecolor=AXCOLOR)
        self.widget = Button(self.axes, name, color=AXCOLOR, hovercolor="0.975")

        for name, func in callback_dict.items():
            self._set_callback(name, func)

    def _set_callback(self, name, func):
        if name == "on_clicked":
            self.widget.on_clicked(func)
        else:
            print("name not found : ", name)


class WidgetRadioButton:
    def __init__(self, rect, labels, callback_dict):
        self.axes = plt.axes(rect, facecolor=AXCOLOR)
        self.widget = RadioButtons(self.axes, labels, active=0)

        for name, func in callback_dict.items():
            self._set_callback(name, func)

    def _set_callback(self, name, func):
        if name == "on_clicked":
            self.widget.on_clicked(func)
        else:
            print("name not found : ", name)


class Sim:
    AXCOLOR = "lightgoldenrodyellow"
    BASE_WINDOW_WH = (9, 6)

    # widget position [left, bottom, width, height]
    AX_RECT_IMG = [0.1, 0.4, 0.8, 0.5]

    AX_RECT_FILLMODE_RADIO = [0.05, 0.4, 0.1, 0.15]

    AX_RECT_ROTATE_SLIDER = [0.15, 0.3, 0.7, 0.02]
    AX_RECT_WSHIFT_SLIDER = [0.15, 0.27, 0.7, 0.02]
    AX_RECT_HSHIFT_SLIDER = [0.15, 0.24, 0.7, 0.02]
    AX_RECT_SHEAR_SLIDER = [0.15, 0.21, 0.7, 0.02]
    AX_RECT_ZOOM_SLIDER = [0.15, 0.18, 0.7, 0.02]
    AX_RECT_INTERVAL_SLIDER = [0.1, 0.1, 0.8, 0.02]

    AX_RECT_OPEN_BUTTON = [0.1, 0.025, 0.1, 0.04]
    AX_RECT_QUIT_BUTTON = [0.2, 0.025, 0.1, 0.04]
    AX_RECT_START_BUTTON = [0.7, 0.025, 0.1, 0.04]
    AX_RECT_STOP_BUTTON = [0.8, 0.025, 0.1, 0.04]

    def __init__(self, img_path):
        self.start = True
        self.quit = False
        self.interval = 0.5

        self.gen_params = {}
        self.gen_params["rotate"] = 0
        self.gen_params["width_shift"] = 0
        self.gen_params["height_shift"] = 0
        self.gen_params["shear"] = 0
        self.gen_params["zoom"] = 0
        self.gen_params["fill_mode"] = "nearest"
        self.init_widgets(img_path)

    def init_widgets(self, img_path):
        self.img = np.asarray(Image.open(img_path))
        # self.img.flags.writeable = True
        self.prev_img = self.img

        self.fig = plt.figure(figsize=self.BASE_WINDOW_WH)
        self.ax_img = plt.axes(self.AX_RECT_IMG)
        plt.axes(self.ax_img)
        plt.title(img_path)
        self.img_plot = plt.imshow(self.img)

        self.slider = {}
        self.slider["rotate"] = WidgetSlider(
            self.AX_RECT_ROTATE_SLIDER,
            "rotate",
            0,
            180,
            0,
            {"on_changed": self.event_slider_changed},
        )
        self.slider["width_shift"] = WidgetSlider(
            self.AX_RECT_WSHIFT_SLIDER,
            "width_shift",
            0,
            1,
            0,
            {"on_changed": self.event_slider_changed},
        )
        self.slider["height_shift"] = WidgetSlider(
            self.AX_RECT_HSHIFT_SLIDER,
            "height_shift",
            0,
            1,
            0,
            {"on_changed": self.event_slider_changed},
        )
        self.slider["shear"] = WidgetSlider(
            self.AX_RECT_SHEAR_SLIDER,
            "shear",
            0,
            180,
            0,
            {"on_changed": self.event_slider_changed},
        )
        self.slider["zoom"] = WidgetSlider(
            self.AX_RECT_ZOOM_SLIDER,
            "zoom",
            0,
            1,
            0,
            {"on_changed": self.event_slider_changed},
        )
        self.slider["interval"] = WidgetSlider(
            self.AX_RECT_INTERVAL_SLIDER,
            "interval",
            0.1,
            1,
            self.interval,
            {"on_changed": self.event_slider_changed},
        )

        self.radio_button = {}
        self.radio_button["fill_mode"] = WidgetRadioButton(
            self.AX_RECT_FILLMODE_RADIO,
            ("nearest", "constant", "reflect", "wrap"),
            {"on_clicked": self.event_fillmode_clicked},
        )

        self.button = {}
        self.button["quit"] = WidgetButton(
            self.AX_RECT_QUIT_BUTTON, "quit", {"on_clicked": self.event_quit_clicked}
        )
        self.button["start"] = WidgetButton(
            self.AX_RECT_START_BUTTON, "start", {"on_clicked": self.event_start_clicked}
        )
        self.button["stop"] = WidgetButton(
            self.AX_RECT_STOP_BUTTON, "stop", {"on_clicked": self.event_stop_clicked}
        )

    def convert(self, x):
        datagen = ImageDataGenerator(
            featurewise_center=False,
            samplewise_center=False,
            fill_mode=self.gen_params["fill_mode"],
            rotation_range=self.gen_params["rotate"],
            width_shift_range=self.gen_params["width_shift"],
            height_shift_range=self.gen_params["height_shift"],
            shear_range=self.gen_params["shear"],
            zoom_range=self.gen_params["zoom"],
            horizontal_flip=False,
            vertical_flip=False,
            rescale=0,
        )

        x = x.reshape((1,) + x.shape)
        for d in datagen.flow(x, batch_size=1):
            return np.uint8(d[0])

    def run(self):
        while True:
            if self.quit:
                break

            if self.start:
                img = self.convert(self.img)

                plt.axes(self.ax_img)
                self.img_plot.set_data(img)

                self.prev_img = img

                plt.pause(self.interval)  # seconds
            else:
                # draw img only
                self.img_plot.set_data(self.prev_img)
                plt.pause(1.0)  # seconds

    def event_slider_changed(self, val):
        # get all slider values
        self.interval = self.slider["interval"].get_val()

        for key in self.gen_params.keys():
            if key in self.slider.keys():
                self.gen_params[key] = self.slider[key].get_val()

    def event_quit_clicked(self, event):
        print("quit")
        self.quit = True

    def event_start_clicked(self, event):
        print("random_erasing : {} -> {}".format(self.start, "True"))
        self.start = True

    def event_stop_clicked(self, event):
        print("random_erasing : {} -> {}".format(self.start, "False"))
        self.start = False

    def event_fillmode_clicked(self, label):
        self.gen_params["fill_mode"] = label


def get_args():
    parser = argparse.ArgumentParser(description="ImageGenerator")
    parser.add_argument("img_path", type=str, help="path2your_image", default=None)
    return parser.parse_args()


def main(args):
    img_path = args.img_path
    sim = Sim(img_path)
    sim.run()


if __name__ == "__main__":
    main(get_args())
