package com.itgo.swing.body;

import com.itgo.swing.component.button.TabCloseButton;

import javax.swing.*;
import java.awt.*;

public class ItgoTabPane {
    private int index;
    private JScrollPane scrollPane;
    private ItgoTabbedPane itgoTabbedPane;

    public ItgoTabPane(String title, Component oneTab, int index, ItgoTabbedPane itgoTabbedPane) {
        this(title, oneTab, index, null, itgoTabbedPane);
    }

    public ItgoTabPane(String title, Component oneTab, int index, Icon icon, ItgoTabbedPane itgoTabbedPane) {

        this.index = index;
        this.itgoTabbedPane = itgoTabbedPane;
        // scroll pane
        scrollPane = new JScrollPane();
        scrollPane.setHorizontalScrollBarPolicy(ScrollPaneConstants.HORIZONTAL_SCROLLBAR_AS_NEEDED);
        scrollPane.setViewportView(oneTab);

        itgoTabbedPane.getTabbedPane().addTab(title, icon, scrollPane, "tab_" + index);

        itgoTabbedPane.getTabbedPane().setTabComponentAt(index, tabTitle(title));
    }


    private JPanel tabTitle(String title) {
        // title
        JPanel panel_tab = new JPanel();
//        panel_tab.setLayout(new GridLayout(1, 2, 10, 0));
        panel_tab.setLayout(new FlowLayout(FlowLayout.LEFT));
        panel_tab.setBorder(BorderFactory.createEmptyBorder(2, 0, 0, 0));
        //不画出panel的边界
        panel_tab.setOpaque(false);

        // label title1
        JLabel label_title = new JLabel(title);
        label_title.setHorizontalAlignment(JLabel.LEFT);
        label_title.setBorder(BorderFactory.createEmptyBorder(0, 0, 0, 5));
        label_title.setOpaque(false);
        panel_tab.add(label_title);

        /*
        // label title2
        JLabel label_close = new JLabel();
        label_close.setSize(12, 12);
        label_close.setOpaque(false);
        URL url_close = ItgoTabPane.class.getResource("/images/close_btn.jpg");
        ImageIcon icon_close = new ImageIcon(url_close);
        icon_close = ImageScale.getImage(icon_close, label_close.getWidth(), label_close.getHeight());
        label_close.setIcon(icon_close);
        label_close.setHorizontalAlignment(JLabel.RIGHT);
        panel_tab.registerKeyboardAction(e -> {
            System.out.println("closing by ctrl+w:" + index);
            // remove tab
            int selectedIndex = itgoTabbedPane.getTabbedPane().getSelectedIndex();
            System.out.println("selected index:" + selectedIndex);
            itgoTabbedPane.removeTab(selectedIndex);
        }, "remove tab", KeyStroke.getKeyStroke(KeyEvent.VK_W, KeyEvent.CTRL_MASK), JComponent.WHEN_IN_FOCUSED_WINDOW);

        // label title2 : add mouse listener
        label_close.addMouseListener(new MouseAdapter() {
            @Override
            public void mousePressed(MouseEvent e) {
                System.out.println("closing by mouse:" + index);
                // remove tab
                itgoTabbedPane.removeTab(scrollPane);
            }
        });
        panel_tab.add(label_close);
        */

        TabCloseButton closeButton = new TabCloseButton(scrollPane, itgoTabbedPane);
        panel_tab.add(closeButton);
        return panel_tab;
    }

}
