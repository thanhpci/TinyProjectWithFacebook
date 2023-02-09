package com.example.demojavafxkteam;

import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.scene.layout.AnchorPane;
import javafx.stage.FileChooser;
import javafx.stage.Stage;

import java.io.File;

public class Controller17 {
    @FXML
    private ImageView imageView;
    @FXML
    private AnchorPane ap;


    public void chooseImage(ActionEvent event) {
        Stage stage = (Stage) ap.getScene().getWindow();
        FileChooser fc = new FileChooser();
        fc.setTitle("Choose a image");
        FileChooser.ExtensionFilter imageFilter = new FileChooser.ExtensionFilter("Image Files", "*.jpg", "*.png");
        fc.getExtensionFilters().add(imageFilter);

        File file = fc.showOpenDialog(stage);

        if (file != null) {
            Image image = new Image(file.toURI().toString(), 143, 102, false, true);
            imageView.setImage(image);
        }



    }


}
