package com.example.demojavafxkteam;


import javafx.application.Application;
import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.scene.Scene;
import javafx.scene.control.Alert;
import javafx.scene.control.Button;
import javafx.scene.control.ButtonBar;
import javafx.scene.control.ButtonType;
import javafx.scene.layout.StackPane;
import javafx.stage.Stage;

import java.util.Optional;

public class Main3 extends Application {

    Button button;


    public static void main(String[] args) {
        launch(args);
    }

    /**
     Alert là bảng thông báo yêu cầu người dùng lựa chọn
     */

    @Override
    public void start(Stage primaryStage) {
        primaryStage.setTitle("Hello World");
        button = new Button();
        button.setText("Close");
        button.setOnAction(new EventHandler<ActionEvent>() {
            @Override
            public void handle(ActionEvent event) {
                Alert alert = new Alert(Alert.AlertType.CONFIRMATION);      //Dạng có quyền lựa chọn
                alert.setTitle("Confirmation");
                alert.setHeaderText("Alert information");
                alert.setContentText("Choose your option");

                ButtonType buttonTypeYes = new ButtonType("Yes", ButtonBar.ButtonData.YES);
                ButtonType buttonTypeNO = new ButtonType("No", ButtonBar.ButtonData.NO);
                ButtonType buttonTypeCancel = new ButtonType("Cancel", ButtonBar.ButtonData.CANCEL_CLOSE);

                alert.getButtonTypes().setAll(buttonTypeYes, buttonTypeNO, buttonTypeCancel);

                Optional<ButtonType> result = alert.showAndWait();

                if (result.get() == buttonTypeYes)
                    System.out.println("Code for yes");
                else if (result.get().getButtonData() == ButtonBar.ButtonData.NO)
                    System.out.println("Code for no");
                else
                    System.out.println("Code for cancel");

                String message = result.get().getText();
                Alert alert1 = new Alert (Alert.AlertType.INFORMATION);
                alert1.setTitle("Information");
                alert1.setHeaderText("Notification");
                alert1.setContentText(message);
                alert1.show();


            }
        });

        StackPane layout = new StackPane();
        layout.getChildren().add(button);
        Scene scene = new Scene(layout, 300, 250);
        primaryStage.setScene(scene);
        primaryStage.show();
    }
}
