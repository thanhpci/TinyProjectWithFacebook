package com.example.demojavafxkteam;

import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.scene.chart.PieChart;
import javafx.scene.control.Alert;
import javafx.scene.control.TextField;
import javafx.scene.input.MouseEvent;

public class Controller19 {
    @FXML
    public TextField CSharpId, JavaId, PythonId;

    @FXML
    PieChart pieChart;

    public void load(ActionEvent e) {
        try {
            int CSharpValue = Integer.parseInt(CSharpId.getText());
            int JavapValue = Integer.parseInt(JavaId.getText());
            int PythonValue = Integer.parseInt(PythonId.getText());

            PieChart.Data CSharp = new PieChart.Data("C#", CSharpValue);
            PieChart.Data Java = new PieChart.Data("Java", JavapValue);
            PieChart.Data Python = new PieChart.Data("Python", PythonValue);

            pieChart.getData().clear();
            pieChart.getData().addAll(CSharp, Java, Python);

            for (PieChart.Data data : pieChart.getData()) {
                data.getNode().addEventHandler(MouseEvent.MOUSE_CLICKED, event -> {
                    Alert alert = new Alert(Alert.AlertType.INFORMATION);
                    alert.setTitle("Data");
                    alert.setContentText(data.getName() + ":" + data.getPieValue());
                    alert.showAndWait();



                });
            }


        } catch (Exception ex) {
            ex.printStackTrace();
        }

    }


}
