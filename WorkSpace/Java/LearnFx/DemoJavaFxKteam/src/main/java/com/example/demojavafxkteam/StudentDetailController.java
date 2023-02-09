package com.example.demojavafxkteam;

import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.Node;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.Label;
import javafx.stage.Stage;

import java.io.IOException;

public class StudentDetailController {
    @FXML
    Label idLabel;

    @FXML
    Label nameLabel;

    @FXML
    Label emailLabel;

    @FXML
    Label ageLabel;


    public void setStudent21(Student21 student21) {
        idLabel.setText(String.valueOf(student21.getId()));
        emailLabel.setText(student21.getEmail());
        nameLabel.setText(student21.getName());
        ageLabel.setText(String.valueOf(student21.getAge()));
    }

    public void goBack(ActionEvent e) throws IOException {
        Stage stage = (Stage) ((Node) e.getSource()).getScene().getWindow();

        FXMLLoader loader = new FXMLLoader();
        loader.setLocation(getClass().getResource("sample21.fxml"));

        Parent root = loader.load();
        Scene scene = new Scene(root);

        stage.setScene(scene);
    }

}












