package com.nilhcem.md2html.gui;

import javax.swing.*;
import java.awt.*;
import java.io.*;

/**
 * Provides the main window of the application.
 */
public final class MainFrame {
	private final JFrame mainFrame = new JFrame("Markdown editor");
	private final MenuBar menu = new MenuBar();
	private final MainPanel panel = new MainPanel();
	private final InputPane input = panel.getInput();
	private JMenuItem open = menu.getChooser();
	private JMenuItem save = menu.getSave();
	private String path, content;


	/**
	 * Creates the main window and makes it visible.
	 */
	public MainFrame() {
		Dimension frameSize = new Dimension(1800, 1000);

		mainFrame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		mainFrame.setSize(frameSize);
		mainFrame.setMinimumSize(frameSize);

		mainFrame.setJMenuBar(menu.get());
		mainFrame.getContentPane().add(panel.get());

		JFileChooser chooser = new JFileChooser();
		open.addActionListener(e ->
				{
					System.out.println("open");
					chooser.setFileSelectionMode(JFileChooser.FILES_ONLY);
					chooser.showOpenDialog(new JLabel("选择"));

					path = chooser.getSelectedFile().getPath();
					System.out.println(path);

					content = readToString(path);
					input.setText(content);
				}
		);

		save.addActionListener(e ->
				{
					int select = JOptionPane.showConfirmDialog(new JFrame().getContentPane(),
							"确定写入？", "Message", JOptionPane.YES_NO_OPTION, JOptionPane.QUESTION_MESSAGE);
					if (select == 0) {
						System.out.println("Write is processing");
						content = input.getText();
						if (!path.equals(""))
							writeString(path, content);
					} else
						System.out.println("Write nothing!");
				}
		);

		mainFrame.setLocationRelativeTo(null); // Center main frame
		mainFrame.setVisible(true);
	}

	private String readToString(String fileName) {
		String encoding = "UTF-8";
		File file = new File(fileName);
		Long filelength = file.length();
		byte[] filecontent = new byte[filelength.intValue()];
		try {
			FileInputStream in = new FileInputStream(file);
			in.read(filecontent);
			in.close();
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
		try {
			return new String(filecontent, encoding);
		} catch (UnsupportedEncodingException e) {
			System.err.println("The OS does not support " + encoding);
			e.printStackTrace();
			return null;
		}
	}

	private void writeString(String path, String con) {

		FileOutputStream fop = null;
		File file;

		try {
			file = new File(path);
			fop = new FileOutputStream(file);
			// if file doesnt exists, then create it
			if (!file.exists()) {
				file.createNewFile();
			}
			// get the content in bytes
			byte[] contentInBytes;
			contentInBytes = con.getBytes();

			fop.write(contentInBytes);
			fop.flush();
			fop.close();

		} catch (IOException e) {
			e.printStackTrace();
		} finally {
			try {
				if (fop != null) {
					fop.close();
				}
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
	}
}
