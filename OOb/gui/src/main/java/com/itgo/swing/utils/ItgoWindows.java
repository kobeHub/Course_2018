package com.itgo.swing.utils;

import java.awt.*;

public class ItgoWindows {

    public static void setWindowsCenter(Container frame) {
        Toolkit kits = Toolkit.getDefaultToolkit();
        Dimension screenSize = kits.getScreenSize();
        int width = (int) screenSize.getWidth();
        int height = (int) screenSize.getHeight();
        int frameWidth = frame.getWidth();
        int frameHeight = frame.getHeight();
        frame.setLocation((width - frameWidth) / 2, (height - frameHeight) / 2);
    }
}
