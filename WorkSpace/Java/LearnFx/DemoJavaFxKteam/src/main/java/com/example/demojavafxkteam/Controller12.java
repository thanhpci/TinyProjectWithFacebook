package com.example.demojavafxkteam;

import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.ComboBox;
import javafx.scene.control.Label;

import java.net.URL;
import java.util.ResourceBundle;

public class Controller12 implements Initializable {
    @FXML
    public ComboBox<String> comboBox;

    @FXML
    public Label label;


    ObservableList<String> list = FXCollections.observableArrayList("Java", "C#", "Python");        //Giống list nhưng bắt thay đổi


    @Override
    public void initialize(URL url, ResourceBundle resourceBundle) {
        comboBox.setItems(list);
    }

    public void comboBoxChanged(ActionEvent e) {
        label.setText(comboBox.getValue());

    }
}
