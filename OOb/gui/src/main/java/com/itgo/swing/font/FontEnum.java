package com.itgo.swing.font;

public enum FontEnum {
    GLOBALFONT("global_font"),LITTLEFONT("little_font"), DEFAULTFONT("default_font"), BIGFONT("big_font");

    private String val;

    public String getVal() {
        return val;
    }

    public void setVal(String val) {
        this.val = val;
    }

    private FontEnum(String val) {
        this.val = val;
    }
}