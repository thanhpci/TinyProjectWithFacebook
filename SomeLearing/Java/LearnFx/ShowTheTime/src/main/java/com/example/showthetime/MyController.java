package com.example.showthetime;

import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;

import java.net.URL;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.ResourceBundle;

public class MyController implements Initializable {

    public Button myButton;
    public TextField myTextField;


    @Override
    public void initialize(URL url, ResourceBundle resourceBundle) {

    }


    //Khi người dùng click vào button hàm này sẽ đc gọi
    public void showDateTime(ActionEvent event) {
        System.out.println("Button clicked!");

        Date now = new Date();
        DateFormat df = new SimpleDateFormat("dd-MM-yyyy HH:mm:ss.SS");

        //Dữ liệu model
        String dateTimeString = df.format(now);

        //Hiển thị lên view
        myTextField.setText(dateTimeString);


    }


}