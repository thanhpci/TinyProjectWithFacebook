package com.example.demojavafxkteam;

import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.fxml.Initializable;
import javafx.scene.Node;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.TableColumn;
import javafx.scene.control.TableView;
import javafx.scene.control.TextField;
import javafx.scene.control.cell.PropertyValueFactory;
import javafx.stage.Stage;

import java.io.IOException;
import java.net.URL;
import java.util.ResourceBundle;

public class Controller21 implements Initializable {
    @FXML
    private TableView<Student21> table;

    @FXML
    private TableColumn<Student21, Integer> idColumn;
    @FXML
    private TableColumn<Student21, String> nameColumn;
    @FXML
    private TableColumn<Student21, String> emailColumn;
    @FXML
    private TableColumn<Student21, Integer> ageColumn;

    private ObservableList<Student21> studentList;


    @FXML private TextField idText;
    @FXML private TextField nameText;
    @FXML private TextField emailText;
    @FXML private TextField ageText;


    @Override
    public void initialize(URL url, ResourceBundle resourceBundle) {
        studentList = FXCollections.observableArrayList(
                new Student21(1, "Chau", "chau@gmail.com", 21),
                new Student21(2, "Thanh", "thanh@gmail.com", 20)
        );

        idColumn.setCellValueFactory(new PropertyValueFactory<Student21, Integer>("id"));
        nameColumn.setCellValueFactory(new PropertyValueFactory<Student21, String>("name"));
        emailColumn.setCellValueFactory(new PropertyValueFactory<Student21, String>("email"));
        ageColumn.setCellValueFactory(new PropertyValueFactory<Student21, Integer>("age"));
        table.setItems(studentList);
    }

    public void add(ActionEvent e) {
        Student21 newStudent21 = new Student21();
        newStudent21.setId(Integer.parseInt(idText.getText()));
        newStudent21.setName(nameText.getText());
        newStudent21.setEmail(emailText.getText());
        newStudent21.setAge(Integer.parseInt(ageText.getText()));

        studentList.add(newStudent21);

    }

    public void delete(ActionEvent e) {
        Student21 selected = table.getSelectionModel().getSelectedItem();
        studentList.remove(selected);
    }

    public void changeScenceStudentDetail(ActionEvent e) throws IOException {
        Stage stage = (Stage) ((Node) e.getSource()).getScene().getWindow();
        FXMLLoader loader = new FXMLLoader();
        loader.setLocation(getClass().getResource("studentDetail.fxml"));
        Parent studentViewParent = loader.load();
        Scene scene = new Scene(studentViewParent);

        StudentDetailController controller = loader.getController();
        Student21 selected = table.getSelectionModel().getSelectedItem();
        controller.setStudent21(selected);


        stage.setScene(scene);


    }

}
