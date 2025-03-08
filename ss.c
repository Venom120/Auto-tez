#include <stdio.h>
#include <stdlib.h>
#include <X11/X.h>
#include <X11/Xlib.h>
#include <X11/Xutil.h>

void getScreen(const int, const int, const int, const int, unsigned char *);
void getScreen(const int xx, const int yy, const int W, const int H, /*out*/ unsigned char *data)
{
    Display *display = XOpenDisplay(NULL);
    Window root = DefaultRootWindow(display);
    XImage *image = XGetImage(display, root, xx, yy, W, H, AllPlanes, ZPixmap);

    unsigned long red_mask = image->red_mask;
    unsigned long green_mask = image->green_mask;
    unsigned long blue_mask = image->blue_mask;
    int x, y;
    int ii = 0;
    for (y = 0; y < H; y++)
    {
        for (x = 0; x < W; x++)
        {
            unsigned long pixel = XGetPixel(image, x, y);
            unsigned char red = (pixel & red_mask) >> 16;
            unsigned char green = (pixel & green_mask) >> 8;
            unsigned char blue = (pixel & blue_mask);
            data[ii + 2] = red;
            data[ii + 1] = green;
            data[ii + 0] = blue;
            ii += 3;
        }
    }

    XDestroyImage(image);
    XCloseDisplay(display);
}
