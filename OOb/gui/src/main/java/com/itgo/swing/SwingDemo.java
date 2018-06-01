package com.itgo.swing;

import com.itgo.swing.beautyeye.ItgoBeautyEye;
import com.itgo.swing.body.ItgoTabbedPane;
import com.itgo.swing.bottom.ItgoBottomPanel;
import com.itgo.swing.font.FontEnum;
import com.itgo.swing.font.ItgoFont;
import com.itgo.swing.menu.ItgoMenuBar;
import com.itgo.swing.test.TestJEditPane;
import com.itgo.swing.test.TestPanel;
import com.itgo.swing.toolbar.ItgoToolBar;

import javax.swing.*;
import java.awt.*;
import java.net.URL;

public class SwingDemo {

    public static void main(String[] args) {
        ItgoBeautyEye.initBeautyEye();
        SwingDemo swingDemo = new SwingDemo();
        swingDemo.init();
    }

    private JFrame frame;
    private Container jConentPanel;
    private JTextArea textArea;
    private int frameWidth = 900;
    private int frameHeight = 600;
    private ItgoTabbedPane itgoTabbedPane = new ItgoTabbedPane();
    private int nameIndex = 0;

    private void init() {
        initFont();
        initFrame();
        initMenu();
        initTools();
        initBody();
        initBottom();
        frame.setVisible(true);
    }

    private void initFont() {
        //set global font
        Font globFont = new Font("SimSun", 0, 14);
        ItgoFont.setFont(FontEnum.GLOBALFONT, globFont);
        // init global font
        ItgoFont.initGlobalFont(ItgoFont.getFont(FontEnum.GLOBALFONT));
    }

    private void initMenu() {
        ItgoMenuBar itgoMenuBar = new ItgoMenuBar();
        // add file Menu
        itgoMenuBar.addFileMenu(itgoTabbedPane);
        itgoMenuBar.addAboutMenu(itgoTabbedPane);
        frame.setJMenuBar(itgoMenuBar.getMenuBar());
    }

    private void initTools() {
        ItgoToolBar toolBar = new ItgoToolBar();
        JPanel toolsPanel = toolBar.addBtnBar(3, jConentPanel).addCommBar(1, jConentPanel).build();
        jConentPanel.add(toolsPanel, BorderLayout.NORTH);
    }

    private void initFrame() {
        frame = new JFrame("Inno Editor");
        frame.setSize(frameWidth, frameHeight);
        // 居中
        frame.setLocationRelativeTo(null);
        jConentPanel = frame.getContentPane();

        // set default close operation
        frame.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
        // set logo
        URL url = SwingDemo.class.getResource("/images/logo_s.jpg");
        ImageIcon iconImage = new ImageIcon(url);
        frame.setIconImage(iconImage.getImage());
    }

    private void initBody() {
        // and one test panel
//        TestPanel testPanel = new TestPanel();
//        itgoTabbedPane.addTab("Editor panel", testPanel.getPanel());

//        TestJEditPane eidtorPane = new TestJEditPane();
//        itgoTabbedPane.addTab("eidtorPane", eidtorPane.getEditorPane());

        // add one TextArea pane
        itgoTabbedPane.addTextAreaTab("tab_1", null, new Color(199, 237, 204));

        // add one TextArea pane
        itgoTabbedPane.addTextAreaTab("tab_2", null, Color.gray);

        jConentPanel.add(itgoTabbedPane.getTabbedPane(), BorderLayout.CENTER);
    }


    private void initBottom() {
        ItgoBottomPanel itgoBottomPanel = new ItgoBottomPanel(this.frame);
        itgoBottomPanel.addBottom();
        this.jConentPanel.add(itgoBottomPanel.getjBottomPanel(), BorderLayout.SOUTH);
    }

    private void registerListener() {
        // TODO
    }

    public int getNameIndex() {
        return nameIndex;
    }

    public void setNameIndex(int nameIndex) {
        this.nameIndex = nameIndex;
    }
}
