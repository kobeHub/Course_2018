package com.itgo.awt;

import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.HashMap;
import java.util.Map;

class ItgoCardEventListener implements ActionListener {

    private Container parent;
    private CardLayout cardLayout;
    private Map<CardOption, Component> componentMap;


    public ItgoCardEventListener(CardLayout cardLayout, Container parent) {
        componentMap = new HashMap<>();
        this.cardLayout = cardLayout;
        this.parent = parent;
    }

    public void addComponent(CardOption option, Component component) {
        if (componentMap != null) {
            componentMap.put(option, component);
        }
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        if (componentMap == null || componentMap.size() == 0) {
            return;
        }
        Object source = e.getSource();
        if (source == componentMap.get(CardOption.FIRST)) {
            cardLayout.first(parent);
        } else if (source == componentMap.get(CardOption.PREVIOUSE)) {
            cardLayout.previous(parent);
        } else if (source == componentMap.get(CardOption.NEXT)) {
            cardLayout.next(parent);
        } else if (source == componentMap.get(CardOption.LAST)) {
            cardLayout.last(parent);
        }
    }
}