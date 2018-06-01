package com.itgo.swing.test;

import com.itgo.swing.LoginDialog;
import com.itgo.swing.SwingDemo;
import org.jb2011.lnf.beautyeye.ch3_button.BEButtonUI;

import javax.swing.*;
import java.awt.*;
import java.io.IOException;
import java.net.URL;

public class TestPanel {
    private JPanel panel;

    public JPanel getPanel() {
        return panel;
    }

    public TestPanel() {
        panel = new JPanel();
        init();
    }

    private void init() {
        panel.setLayout(new GridLayout(7, 1));

        JPanel pan0 = new JPanel();
        JButton loginButton = new JButton("login");
        loginButton.setUI(new BEButtonUI().setNormalColor(BEButtonUI.NormalColor.lightBlue));
        loginButton.addActionListener(e -> {
            LoginDialog loginDialog = new LoginDialog(true);
            URL url = SwingDemo.class.getResource("/images/logo_s.jpg");
            ImageIcon iconImage = new ImageIcon(url);
            loginDialog.setIconImage(iconImage.getImage());
            loginDialog.setVisible(true);
        });

//        pan0.add(loginButton);
        panel.add(pan0);

    }
}
