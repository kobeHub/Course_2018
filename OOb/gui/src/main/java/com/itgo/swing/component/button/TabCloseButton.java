package com.itgo.swing.component.button;

import com.itgo.swing.body.ItgoTabbedPane;

import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class TabCloseButton extends JButton implements ActionListener {
    private final int size = 16;
    private ItgoTabbedPane itgoTabbedPane;
    private JScrollPane scrollPane;

    public TabCloseButton(JScrollPane scrollPane, ItgoTabbedPane itgoTabbedPane) {
        this.itgoTabbedPane = itgoTabbedPane;
        this.scrollPane = scrollPane;
        setPreferredSize(new Dimension(size, size));
        this.setForeground(Color.RED);
        this.setBackground(Color.RED);
        this.setText("X");
        //设置按键的提示信息
        setToolTipText("关闭窗口");
        //设置按键的绘制于普通按键相同
//        setUI(new BasicButtonUI());
        //不对Button进行填充，就是按键是透明的
        setContentAreaFilled(false);
        //按键不能获得焦点
        setFocusable(false);
        //设置按键的边框为雕刻样式
        setBorder(BorderFactory.createEtchedBorder());
        //系统不自动绘制按键边界（这个边界在鼠标放上去之后才绘制）
        setBorderPainted(false);

        this.addActionListener(TabCloseButton.this);

        this.addMouseListener(new MouseAdapter() {
            @Override
            public void mouseEntered(MouseEvent e) {
                //鼠标移入按键，绘制按键边界
                Component c = e.getComponent();
                if (c instanceof AbstractButton)
                    ((AbstractButton) c).setBorderPainted(true);
            }

            @Override
            public void mouseExited(MouseEvent e) {
                //鼠标移出按键，不绘制按键边界
                Component c = e.getComponent();
                if (c instanceof AbstractButton)
                    ((AbstractButton) c).setBorderPainted(false);
            }
        });

        this.registerKeyboardAction(e -> {
            // remove tab
            int selectedIndex = itgoTabbedPane.getTabbedPane().getSelectedIndex();
            System.out.println("selected index:" + selectedIndex);
            itgoTabbedPane.removeTab(selectedIndex);
        }, "remove tab", KeyStroke.getKeyStroke(KeyEvent.VK_W, KeyEvent.CTRL_MASK), JComponent.WHEN_IN_FOCUSED_WINDOW);

    }

    @Override
    public void actionPerformed(ActionEvent e) {
        System.out.println("button closing");
        itgoTabbedPane.removeTab(scrollPane);
    }

//    @Override
//    public void paintComponents(Graphics g) {
//        super.paintComponents(g);
//        //创建一个graphics2D，因为需要在Button上画差
//        Graphics2D g2 = (Graphics2D) g.create();
//
//        //设置画笔，宽度为2
//        g2.setStroke(new BasicStroke(6));
//        //设置画笔颜色
//        g2.setColor(Color.BLACK);
//        //当鼠标移动到Button上时，画笔为紫色
//        if (getModel().isRollover())
//            g2.setColor(Color.PINK);
//        //绘制差
//        int delta = 10;
//        g2.drawLine(delta, delta, getWidth() - delta - 1, getHeight() - delta - 1);
//        g2.drawLine(getWidth() - delta - 1, delta, delta, getHeight() - delta - 1);
//        //释放画笔资源
//        g2.dispose();
//    }
}
