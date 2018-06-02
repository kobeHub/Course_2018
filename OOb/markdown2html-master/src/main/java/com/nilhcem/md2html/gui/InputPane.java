package com.nilhcem.md2html.gui;

import javax.swing.*;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.util.Observable;

/**
 * Scrolled text area where will be inputed markdown data to be converted.
 */
public final class InputPane extends Observable {
	private final JScrollPane inputPane = new JScrollPane();
	private final JTextArea inputTextArea = new JTextArea();
	private final String initContent;

	/**
	 * Creates the text area and add a key listener to call observer every time a key is released.
	 */
	public InputPane() {
		inputPane.getViewport().add(inputTextArea, null);
		initContent = "# Welcome to Inno Markdown Editor\n" +
				"\n" +
				"##What's Inno Markdown Editor? \n" +
				"\n" +
				"<br><br>\n" +
				"*Inno markdown editor is a simple, light-weight,* \n" +
				"<br>*cross-platform, multilingual Markdown document processing tools*\n" +
				"\n" +
				"\n" +
				"<br><br>\n" +
				"## 特点：\n" +
				"\n" +
				"+ 支持markdown基本的语法属性，サポート日本語（支持日语），Поддержка русского языка(支持俄语)......\n" +
				"<br>等各种全球通用语言的编辑\n" +
				"+ 提供实时的markdown 向html格式转换，以供用户进行实时的预览\n" +
				"+ 支持图片，超链接，不同字体格式以及自定义排版\n" +
				"+ 高效文档产出工具，提供便利的博客书写\n" +
				"\n" +
				"##TODO:\n" +
				"+ 导出html到blog\n" +
				"+ 部分语法的未实现，如表情，多选框等等\n" +
				"\n" +
				"\n" +
				"<br><br>\n" +
				"![image](/home/kobe/图片/Wallpapers/opear.jpg)\n" +
				"<br><br>\n" +
				"**Just text and try yourself!**\n" +
				"\n" +
				"**[Author:Inno Jia](http://www.innohub.top/)**\n" +
				"\n" +
				"\n" +
				"\n" +
				"\n" +
				"\n" +
				"\n" +
				"\n" +
				"\n" +
				"\n" +
				"\n" +
				"\n" +
				"\n" +
				"\n" +
				"\n" +
				"\n";

		inputTextArea.setText(initContent);
		setChanged();
		notifyObservers(inputTextArea.getText());
		inputTextArea.addKeyListener(new KeyListener() {
			@Override
			public void keyTyped(KeyEvent e) {
			}

			@Override
			public void keyReleased(KeyEvent e) {
				setChanged();
				notifyObservers(inputTextArea.getText());
			}

			@Override
			public void keyPressed(KeyEvent e) {
			}
		});
	}

	/**
	 * Returns the JScrollPane object.
	 *
	 * @return the JScrollPane object.
	 */
	public JScrollPane get() {
		return inputPane;
	}

	public String getText() {
		return inputTextArea.getText();
	}

	public void setText(String content) {
		inputTextArea.setText(content);
	}
}
