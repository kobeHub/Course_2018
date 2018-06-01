package com.itgo.swing.menu;

import com.itgo.swing.body.ItgoTabbedPane;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyEvent;
import java.net.URL;

public class ItgoMenuBar {
    private JMenuBar menuBar = new JMenuBar();
    private int nameIndex;

    public JMenuBar getMenuBar() {
        return menuBar;
    }

    public void addFileMenu(ItgoTabbedPane itgoTabbedPane) {
        if (itgoTabbedPane == null) return;

        JMenu menu = new JMenu("文件");
        // new
        JMenuItem item_new = new JMenuItem("新建");

        item_new.setAccelerator(KeyStroke.getKeyStroke(KeyEvent.VK_N, KeyEvent.CTRL_MASK));
        item_new.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                itgoTabbedPane.addTextAreaTab("new " + (++nameIndex));
                itgoTabbedPane.getTabbedPane().setSelectedIndex(itgoTabbedPane.getTabIndex() - 1);
            }
        });

        item_new.registerKeyboardAction((e) -> {
            itgoTabbedPane.addTextAreaTab("new " + (++nameIndex));
            itgoTabbedPane.getTabbedPane().setSelectedIndex(itgoTabbedPane.getTabIndex() - 1);
        }, KeyStroke.getKeyStroke(KeyEvent.VK_N, KeyEvent.CTRL_MASK), JComponent.WHEN_IN_FOCUSED_WINDOW);


        // save
        JMenuItem item_save = new JMenuItem("保存");
        item_save.setAccelerator(KeyStroke.getKeyStroke(KeyEvent.VK_S, KeyEvent.CTRL_MASK));

        // exit
        JMenuItem item_exit = new JMenuItem("退出");
        menu.add(item_new);
        menu.add(item_save);
        menu.addSeparator();
        menu.add(item_exit);
        menuBar.add(menu);
    }

    public void addAboutMenu(ItgoTabbedPane itgoTabbedPane) {
        JMenu menu = new JMenu("?");

        JMenuItem item_about = new JMenuItem("关于");
        item_about.addActionListener(e -> {
            URL url = ItgoMenuBar.class.getResource("/images/logo_s.jpg");
            ImageIcon imageIcon = new ImageIcon(url);
            String message = "<html><font color=red>Inno: Rich text Editor</h2></html>";
            JOptionPane.showMessageDialog(itgoTabbedPane.getTabbedPane(), message, "Swing关于", JOptionPane.OK_OPTION, imageIcon);
        });
        menu.add(item_about);
        menuBar.add(menu);
    }
}
