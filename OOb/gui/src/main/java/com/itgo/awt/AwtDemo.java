package com.itgo.awt;

import java.awt.*;
import java.awt.event.*;

public class AwtDemo {
    public static void main(String[] args) {
        AwtDemo awtDemo = new AwtDemo();
        awtDemo.init();
        awtDemo.registListener();

    }

    private Frame frame;
    private Panel panel_top;
    private Panel panel_body;
    private Panel panel_bottom;
    private MenuBar menu_bar;
    private Menu menu_file;
    private MenuItem item_file_new;
    private MenuItem item_file_open;
    private MenuItem item_file_exit;
    private Button button_first;
    private Button button_previous;
    private Button button_next;
    private Button button_last;
    private Button button_test;

    private TextArea textArea;


    private CardLayout bodyCardLayout;

    private void init() {
        initFrame();
        initMenuBar();
        initTop();
        initCenter();
        initBottom();
        frame.setVisible(true);
    }

    private void initFrame() {
        frame = new Frame("AWT_Title");
        frame.setSize(500, 400);
        // show in center
        Toolkit defaultToolkit = Toolkit.getDefaultToolkit();
        int width = (int) defaultToolkit.getScreenSize().getWidth();
        int height = (int) defaultToolkit.getScreenSize().getHeight();
        int frameWidth = frame.getWidth();
        int frameHeight = frame.getHeight();
        frame.setLocation((width - frameWidth) / 2, (height - frameHeight) / 2);
    }

    private void initMenuBar() {
        // panel
        menu_bar = new MenuBar();
        menu_file = new Menu("file");
        item_file_new = new MenuItem("new");
        item_file_open = new MenuItem("open");
        item_file_exit = new MenuItem("exit");
        menu_file.add(item_file_new);
        menu_file.add(item_file_open);
        menu_file.add(item_file_exit);
        menu_bar.add(menu_file);
        frame.setMenuBar(menu_bar);
    }

    private void initTop() {

        panel_top = new Panel();
        button_test = new Button("test");
        panel_top.add(button_test);
        button_test.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                System.out.println("test");
                exit();
            }
        });

        frame.add(panel_top, BorderLayout.NORTH);
    }

    private void initCenter() {
        panel_body = new Panel();
        bodyCardLayout = new CardLayout();
        panel_body.setLayout(bodyCardLayout);

        Label labelOne = new Label("Label One", Label.CENTER);
        labelOne.setBackground(Color.yellow);
        panel_body.add(labelOne);
        // card two
        ScrollPane scrollPane = new ScrollPane();
        textArea = new TextArea();
        scrollPane.add(textArea);
        panel_body.add(scrollPane);

        // card three
        TextField mouseLocation = new TextField();
        mouseLocation.setColumns(20);
        Label labelTwo = new Label("Label Two");
        Panel panel_card3 = new Panel();
        panel_card3.add(labelTwo);
        panel_card3.add(mouseLocation);
        panel_card3.setBackground(Color.cyan);
        panel_body.add(panel_card3);
        panel_body.add(new Label("Label Three"));

        // add mouse listener
        textArea.addMouseListener(new MouseAdapter() {
            @Override
            public void mouseClicked(MouseEvent e) {
                String text = textArea.getText();
                System.out.println("default:" + text);
            }
        });

        labelOne.addMouseMotionListener(new MouseAdapter() {
            @Override
            public void mouseMoved(MouseEvent e) {
                labelOne.setText("mouseMoved" + e.getX() + "," + e.getY());
            }
        });

        panel_card3.addMouseListener(new MouseAdapter() {

            @Override
            public void mousePressed(MouseEvent e) {
                mouseLocation.setText("mousePressed" + e.getX() + "," + e.getY());

            }

            @Override
            public void mouseEntered(MouseEvent e) {

                mouseLocation.setText("mouseEntered" + e.getX() + "," + e.getY());
            }

            @Override
            public void mouseMoved(MouseEvent e) {
                mouseLocation.setText("mouseMoved" + e.getX() + "," + e.getY());
            }

            @Override
            public void mouseWheelMoved(MouseWheelEvent e) {
                mouseLocation.setText("mouseWheelMoved" + e.getX() + "," + e.getY());
            }

            @Override
            public void mouseExited(MouseEvent e) {
                mouseLocation.setText("mouseExited" + e.getX() + "," + e.getY());
            }
        });


        frame.add(panel_body, BorderLayout.CENTER);
    }

    private void initBottom() {
        panel_bottom = new Panel();
        button_first = new Button("first");
        button_previous = new Button("previous");
        button_next = new Button("next");
        button_last = new Button("last");
        panel_bottom.add(button_first);
        panel_bottom.add(button_previous);
        panel_bottom.add(button_next);
        panel_bottom.add(button_last);
        frame.add(panel_bottom, BorderLayout.SOUTH);
    }

    private void registListener() {
        this.frame.addWindowListener(new WindowAdapter() {
            @Override
            public void windowClosing(WindowEvent e) {

                System.out.println("exit");
                System.exit(0);
            }
        });
        ItgoCardEventListener cardBtnEventListener = new ItgoCardEventListener(this.bodyCardLayout, this.panel_body);
        cardBtnEventListener.addComponent(CardOption.FIRST, this.button_first);
        cardBtnEventListener.addComponent(CardOption.PREVIOUSE, this.button_previous);
        cardBtnEventListener.addComponent(CardOption.NEXT, this.button_next);
        cardBtnEventListener.addComponent(CardOption.LAST, this.button_last);

        this.button_first.addActionListener(cardBtnEventListener);
        this.button_previous.addActionListener(cardBtnEventListener);
        this.button_next.addActionListener(cardBtnEventListener);
        this.button_last.addActionListener(cardBtnEventListener);
    }

    private void exit() {
        if (this.textArea != null && this.textArea.getText().length() != 0) {
        } else {
            System.out.println("no data");
        }
    }
}

