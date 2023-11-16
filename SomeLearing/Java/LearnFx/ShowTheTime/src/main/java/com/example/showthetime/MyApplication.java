package com.example.showthetime;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.stage.Stage;

import java.io.IOException;
import java.util.Objects;

public class MyApplication extends Application {
    @Override
    public void start(Stage primaryStage) {
        try {
            //Đọc file fxml và vẽ giao diện

            Parent root = FXMLLoader.load(Objects.requireNonNull(getClass().getResource("Demo1.fxml")));

            primaryStage.setTitle("My application");
            primaryStage.setScene(new Scene(root));
            primaryStage.show();

        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) {
        launch(args);
    }
}