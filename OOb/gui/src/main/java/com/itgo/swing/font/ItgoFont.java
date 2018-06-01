package com.itgo.swing.font;

import javax.swing.*;
import javax.swing.plaf.FontUIResource;
import java.awt.*;
import java.util.Enumeration;
import java.util.HashMap;
import java.util.Map;

public class ItgoFont {

    private static Map<String, Font> fontMap = new HashMap<>();

    public static void setFont(String key, Font font) {
        fontMap.put(key, font);
    }

    public static void setFont(FontEnum keyEnum, Font font) {
        fontMap.put(keyEnum.getVal(), font);
    }

    public static void setFont(String key, String fontStyle, int weight, int size) {
        fontMap.put(key, new Font(fontStyle, weight, size));
    }

    public static Font getFont(String key) {
        Font font = fontMap.get(key);
        if (font != null) {
            return font;
        }
        font = new Font("SimSun", Font.PLAIN, 12);

        fontMap.put(key, font);
        return font;
    }

    public static Font getFont(FontEnum keyenum) {
        Font font = fontMap.get(keyenum.getVal());
        if (font != null) {
            return font;
        }
        switch (keyenum) {
            case LITTLEFONT:
                font = new Font("SimSun", Font.BOLD, 9);
                break;
            case DEFAULTFONT:
                font = new Font("SimSun", Font.BOLD, 12);
                break;
            case BIGFONT:
                font = new Font("SimSun", Font.BOLD, 20);
                break;
            default:
                font = new Font("SimSun", Font.BOLD, 12);
                break;
        }

        fontMap.put(keyenum.getVal(), font);
        return font;
    }

    public static void initGlobalFont(Font font) {
        FontUIResource fontRes = new FontUIResource(font);
        for (Enumeration<Object> keys = UIManager.getDefaults().keys();
             keys.hasMoreElements(); ) {
            Object key = keys.nextElement();
            Object value = UIManager.get(key);
            if (value instanceof FontUIResource) {
                UIManager.put(key, fontRes);
            }
        }
    }
}
