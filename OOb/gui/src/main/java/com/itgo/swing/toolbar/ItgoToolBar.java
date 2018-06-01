package com.itgo.swing.toolbar;

import javax.swing.*;
import java.awt.*;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;
import java.util.HashMap;
import java.util.Map;
import java.util.TreeMap;

public class ItgoToolBar {
    private JPanel toolsPane = new JPanel();
    private Map<Integer, JToolBar> sortMap = new TreeMap<>();

    public JPanel getToolsPane() {
        return toolsPane;
    }

    public ItgoToolBar addBtnBar(int index, Component parentComponent) {
        JToolBar toolBar = new JToolBar("t1");
        JButton bt1 = new JButton("tool1");
        JButton bt2 = new JButton("tool2");
        JButton bt3 = new JButton("tool3");
        JButton bt4 = new JButton("tool4");
        bt1.setMnemonic(KeyEvent.VK_1);
        bt1.addActionListener(e -> {
            int result = JOptionPane.showConfirmDialog(parentComponent, "tool1 buuton", "confirim dialog", JOptionPane.OK_CANCEL_OPTION);
            switch (result) {
                case JOptionPane.OK_OPTION:
                    System.out.println("Select ok");
                    break;

                case JOptionPane.CANCEL_OPTION:
                    System.out.println("select cancel");
                    break;
            }

        });
        bt2.registerKeyboardAction((e) -> {
            JOptionPane.showMessageDialog(parentComponent, "Tool2 button", "info", JOptionPane.INFORMATION_MESSAGE);
        }, KeyStroke.getKeyStroke(KeyEvent.VK_2, 0), JComponent.WHEN_IN_FOCUSED_WINDOW);

        bt2.addActionListener(e -> {
            JOptionPane.showMessageDialog(parentComponent, "Tool2 button", "info", JOptionPane.INFORMATION_MESSAGE);
        });

        bt3.addKeyListener(new KeyAdapter() {
            @Override
            public void keyPressed(KeyEvent e) {
                int keyCode = e.getKeyCode();
                if (keyCode == KeyEvent.VK_3) {
                    JOptionPane.showMessageDialog(parentComponent, "Tool3 button", "info", JOptionPane.INFORMATION_MESSAGE);
                }
            }
        });

        bt4.addActionListener(e -> {
            System.out.println("bt4 actionListener doing");
        });

//        bt4.setAction(new AbstractAction() {
//            @Override
//            public void actionPerformed(ActionEvent e) {
//                System.out.println("bt4 action doing");
//            }
//        });

        toolBar.add(bt1);
        toolBar.add(bt2);
        toolBar.add(bt3);
        toolBar.add(bt4);
        sortMap.put(index, toolBar);
        return this;
    }

    public ItgoToolBar addCommBar(int index, Component parentComponent) {
        JToolBar toolBar = new JToolBar("comm");
        JButton comm_1 = new JButton("comm_1");
        JButton comm_2 = new JButton("comm_2");
        toolBar.add(comm_1);
        toolBar.add(comm_2);
        sortMap.put(index, toolBar);
        return this;
    }

    public JPanel build() {
        if (sortMap.size() == 0) {
            return null;
        }
        toolsPane.setLayout(new FlowLayout(FlowLayout.LEFT, 0, 0));

        sortMap.forEach((index, jToolBar) -> {
            toolsPane.add(jToolBar);
        });
        return this.toolsPane;
    }
}
