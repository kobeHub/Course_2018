package com.itgo.swing.body;

import javax.swing.*;
import java.awt.*;

public class ItgoTabbedPane {
    private int tabIndex = 0;

    public int getTabIndex() {
        return tabIndex;
    }

    private JTabbedPane tabbedPane;

    public JTabbedPane getTabbedPane() {
        return tabbedPane;
    }

    public ItgoTabbedPane() {
        tabbedPane = new JTabbedPane();
    }

    public void addTextAreaTab(String title) {
        // new tab
        this.addTextAreaTab(title, null, null);
    }

    public void addTextAreaTab(String title, Icon icon, Color bgColor) {
        // textArea
        JTextArea textArea = new JTextArea();
        textArea.setBackground(bgColor);
        textArea.setFont(new Font("SimSun", Font.PLAIN, 16));
        // new tab
        new ItgoTabPane(title, textArea, tabIndex++, icon, this);
    }

    public void addTab(String title, Component oneTab) {
        new ItgoTabPane(title, oneTab, tabIndex++, this);
    }

    public void addTab(String title, Component oneTab, Icon icon) {
        new ItgoTabPane(title, oneTab, tabIndex++, icon, this);
    }

    public void removeTab(Component compent) {
        int index = tabbedPane.indexOfComponent(compent);
        System.out.println("closing index:"+index);
        if (index < 0) {
            System.out.println("closing error");
        } else {
            tabbedPane.removeTabAt(index);
            this.tabIndex--;
        }
    }

    public void removeTab(int index) {
        System.out.println("closing index:"+index);
        if (index < 0 || index > tabIndex) {
            System.out.println("closing error");
        } else {
            tabbedPane.removeTabAt(index);
            this.tabIndex--;
        }
    }
}
