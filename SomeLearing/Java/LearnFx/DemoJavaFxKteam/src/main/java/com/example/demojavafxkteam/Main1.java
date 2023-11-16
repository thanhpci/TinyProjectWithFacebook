package com.example.demojavafxkteam;

import javafx.application.Application;
import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.layout.StackPane;
import javafx.stage.Stage;

public class Main1 extends Application {

    Button button;

    public static void main(String[] args) {
        launch(args);
    }

    @Override
    public void start(Stage primaryStage) {         //khởi động khi tạo giao diện
        primaryStage.setTitle("Hello World");       //Sân khấu được truyền vào là primaryStage

        button = new Button();               //Tạo nút
        button.setText("Say Hello World");          //Tạo text trong nó

        button.setOnAction(new EventHandler<ActionEvent>() {        //handle event of button
            @Override
            public void handle(ActionEvent event) {
                System.out.println("Hello Thanh ahihi");
            }
        });

        StackPane layout = new StackPane();         //Layout cách bố trí các control cho 1 scene
        layout.getChildren().add(button);           // đưa button vào

        Scene scene = new Scene(layout, 300, 250);  //Tạo scene và đưa layout vào

        primaryStage.setScene(scene);       //truyền scene vào stage
        primaryStage.show();                //show stage to screen
    }

}
