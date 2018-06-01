package com.itgo.swing.beautyeye;

import org.jb2011.lnf.beautyeye.BeautyEyeLNFHelper;

import javax.swing.*;
import javax.swing.plaf.InsetsUIResource;
import java.awt.*;

public class ItgoBeautyEye {

    public static void initBeautyEye() {
        try {
//            BeautyEyeLNFHelper.frameBorderStyle = BeautyEyeLNFHelper.frameBorderStyle.translucencyAppleLike;
//            org.jb2011.lnf.beautyeye.BeautyEyeLNFHelper.launchBeautyEyeLNF();
//            UIManager.put("RootPane.setupButtonVisible", false);
//            //设置此开关量为false即表示关闭之，BeautyEye LNF中默认是true
//            BeautyEyeLNFHelper.translucencyAtFrameInactive = true;
//            UIManager.put("TabbedPane.tabAreaInsets", new javax.swing.plaf.InsetsUIResource(3, 1, 2, 20));

            BeautyEyeLNFHelper.frameBorderStyle = BeautyEyeLNFHelper.FrameBorderStyle.osLookAndFeelDecorated;
            BeautyEyeLNFHelper.launchBeautyEyeLNF();
            UIManager.put("RootPane.setupButtonVisible", false);
            UIManager.put("TabbedPane.tabAreaInsets", new InsetsUIResource(0, 0, 0, 0));
            UIManager.put("TabbedPane.contentBorderInsets", new InsetsUIResource(0, 0, 2, 0));
            UIManager.put("TabbedPane.tabInsets", new InsetsUIResource(3, 10, 9, 10));
            Font frameTitleFont = (Font) UIManager.get("InternalFrame.titleFont");
            frameTitleFont = frameTitleFont.deriveFont(Font.PLAIN);
            UIManager.put("InternalFrame.titleFont", frameTitleFont);
        } catch (Exception e) {
            System.out.println("load beauty eye fail！");
        }
    }
}
