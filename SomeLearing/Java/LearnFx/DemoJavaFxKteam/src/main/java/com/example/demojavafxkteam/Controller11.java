package com.example.demojavafxkteam;

import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.TreeItem;
import javafx.scene.control.TreeView;

import java.net.URL;
import java.util.ResourceBundle;

public class Controller11 implements Initializable {

    @FXML
    TreeView<String> treeView;


    @Override
    public void initialize(URL url, ResourceBundle resourceBundle) {
        TreeItem<String> root = new TreeItem<>();
        TreeItem<String> JavaFXTutorials = new TreeItem<>("JavaFXTutorials");
        TreeItem<String> sample = new TreeItem<>("sample");
        TreeItem<String> main8 = new TreeItem<>("main8");
        TreeItem<String> main9 = new TreeItem<>("main9");
        TreeItem<String> main10 = new TreeItem<>("main0");

        sample.getChildren().addAll(main8, main9, main10);
        JavaFXTutorials.getChildren().addAll(sample);
        root.getChildren().add(JavaFXTutorials);

        root.setExpanded(true);
        sample.setExpanded(true);

        treeView.setRoot(root);
        treeView.setShowRoot(false);
        treeView.getSelectionModel().selectedItemProperty().addListener((observableValue, oldValue, newValue) -> {
            System.out.println(newValue.getValue()) ;
        });
    }
}
