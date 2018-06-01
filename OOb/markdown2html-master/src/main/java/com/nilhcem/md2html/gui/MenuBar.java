package com.nilhcem.md2html.gui;

import javax.swing.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.Observable;

import static java.lang.System.exit;

/**
 * Provides the menu bar of the application.
 */
public final class MenuBar extends Observable {
    private final JMenuBar menuBar = new JMenuBar();
    private JMenuItem open, save;


    /**
     * Creates the menu bar and the different menus (file / edit / help).
     */
    public MenuBar() {
        menuBar.add(createFileMenu());
        menuBar.add(createHelpMenu());
    }

    /**
     * Returns the JMenuBar object.
     *
     * @return the JMenuBar object.
     */
    public JMenuBar get() {
        return menuBar;
    }

    /**
     * Creates the file menu.
     * <p>
     * The file menu contains an "Exit" item, to quit the application.
     * </p>
     *
     * @return the newly created file menu.
     */
    private JMenu createFileMenu() {
        JMenu fileMenu = new JMenu("File");
        fileMenu.setMnemonic('F');

        open = new JMenuItem("open");
//		JFileChooser chooser = new JFileChooser();
        open.setMnemonic('o');
		/*
		open.addActionListener(e->
                {
                    out.println("open");
                    chooser.setFileSelectionMode(JFileChooser.FILES_ONLY);
                    chooser.showOpenDialog(new JLabel("选择"));

                    path = chooser.getSelectedFile().getPath();
                    out.println(path);
                }
        );*/

        save = new JMenuItem("Save");
        save.setMnemonic('S');

        JMenuItem exit = new JMenuItem("Exit");
        exit.setMnemonic('x');
        exit.addActionListener((e) -> exit(0));

        fileMenu.add(open);
        fileMenu.add(save);
        fileMenu.add(exit);
        return fileMenu;
    }

    /**
     * @return the load file
     */
    public JMenuItem getChooser() {
        return open;
    }

    public JMenuItem getSave() {
        return save;
    }

    /**
     * Creates the help menu.
     * <p>
     * The help menu contains an "About" item, to display some software information.
     * </p>
     *
     * @return the newly created help menu.
     */
    private JMenu createHelpMenu() {
        JMenu helpMenu = new JMenu("Help");
        helpMenu.setMnemonic('h');

        JMenuItem about = new JMenuItem("About");
        about.setMnemonic('a');
        about.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                JOptionPane.showMessageDialog(menuBar.getParent(),
                        String.format("<html><font size=5, color=blue>A simple markdown to html transfer</h2></html>"),
                        "Markdown2HTML", JOptionPane.INFORMATION_MESSAGE);
            }
        });

        helpMenu.add(about);
        return helpMenu;
    }
}
