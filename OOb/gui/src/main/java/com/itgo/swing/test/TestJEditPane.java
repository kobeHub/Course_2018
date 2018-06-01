package com.itgo.swing.test;

import javax.swing.*;
import java.io.IOException;

public class TestJEditPane {
    private JEditorPane editorPane;

    public JEditorPane getEditorPane() {
        return editorPane;
    }

    public TestJEditPane() {
        initEditPane();
    }

    private void initEditPane() {
        editorPane = new JEditorPane();
        editorPane.setEditable(false);
        try {
            editorPane.setPage("https://www.baidu.top/");
        } catch (IOException e) {
            e.printStackTrace();
        }

    }
}
