package com.example.demojavafxkteam;

import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.Slider;
import javafx.scene.control.TextField;
import javafx.util.converter.NumberStringConverter;

import java.net.URL;
import java.util.ResourceBundle;

public class Controller14 implements Initializable {
    @FXML
    public Slider slider;
    public TextField textField;


    public static final double INIT_VALUE = 50;
    @Override
    public void initialize(URL url, ResourceBundle resourceBundle) {
        slider.setValue(INIT_VALUE);
        textField.setText(String.valueOf(INIT_VALUE));
        slider.setMax(200);
        textField.textProperty().bindBidirectional(slider.valueProperty(), new NumberStringConverter());

    }
}
