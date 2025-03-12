# PhotoEditorGUI

## Description

This Python script implements a simple photo editor GUI using the `customtkinter` library for the interface and `PIL` (Pillow) and `cv2` (OpenCV) for image processing. It allows users to load an image, apply various filter kernels (sharpen, blur, edge detection, and motion blur), adjust the filter strength using a slider, reset the image to its original state, and save the edited image.

## Features

-   **Image Loading:** Users can specify the path to an image file, which is then loaded and displayed in the GUI.
-   **Kernel-based Filters:** Implements several common image filtering operations using convolution kernels:
    -   Sharpen
    -   Blur
    -   Edge Detection
    -   Motion Blur
-   **Filter Strength Adjustment:** A slider allows users to control the intensity of the applied filters.
-   **Real-time Preview:** The image display updates in real-time to reflect the applied filters.
-   **Reset Functionality:** Users can revert the image to its original state.
-   **Saving Images:** The edited image can be saved to a specified location.

## Requirements

-   Python 3.6+
-   customtkinter
-   Pillow (PIL)
-   opencv-python

You can install the required packages using pip:

pip install customtkinter Pillow opencv-python

3.  Enter the path to an image in the text box and click "Get Image Path".
4.  Use the slider to adjust the filter strength.
5.  Click the filter buttons to apply effects.
6.  Click "Reset" to revert to the original image.
7.  Click "Save" to save the edited image.
