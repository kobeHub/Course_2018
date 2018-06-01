package com.itgo.swing.bottom;

import javax.swing.*;
import java.awt.*;

public class ItgoBottomPanel {

    private JPanel jBottomPanel;
    private Container parentContainer;

    public JPanel getjBottomPanel() {
        return jBottomPanel;
    }

    public ItgoBottomPanel(Container parentContainer) {
        this.parentContainer = parentContainer;
        jBottomPanel = new JPanel(new GridLayout(1,2));
    }

    public void addBottom() {
        addLeftBottom();
        addRightBottom();
    }

    public void addLeftBottom() {
        JPanel lPanel = new JPanel();
        lPanel.setLayout(new FlowLayout(FlowLayout.LEFT));

        JLabel label1 = new JLabel("status_1");
        lPanel.add(label1);
        lPanel.add(new JSeparator(JSeparator.VERTICAL));
        jBottomPanel.add(lPanel);
    }

    public void addRightBottom() {
        JPanel rPanel = new JPanel();
        rPanel.setLayout(new FlowLayout(FlowLayout.RIGHT));

        JPanel rBoxPanel = new JPanel();
        rBoxPanel.setLayout(new BoxLayout(rBoxPanel, BoxLayout.X_AXIS));

        JLabel label2 = new JLabel("status_2");

        JLabel label3 = new JLabel("status_3");

        JLabel label4 = new JLabel("status_4");

        JLabel label5 = new JLabel("status_5");

        JLabel label6 = new JLabel("status_6");

        rBoxPanel.add(label2);
        rBoxPanel.add(new JSeparator(JSeparator.VERTICAL));
        rBoxPanel.add(label3);
        rBoxPanel.add(new JSeparator(JSeparator.VERTICAL));
        rBoxPanel.add(label4);
        rBoxPanel.add(new JSeparator(JSeparator.VERTICAL));
        rBoxPanel.add(label5);
        rBoxPanel.add(new JSeparator(JSeparator.VERTICAL));
        rBoxPanel.add(label6);
        rPanel.add(rBoxPanel);

        jBottomPanel.add(rPanel);
    }
}
