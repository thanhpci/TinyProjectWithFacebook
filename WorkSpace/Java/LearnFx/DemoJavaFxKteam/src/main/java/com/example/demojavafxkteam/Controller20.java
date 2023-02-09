package com.example.demojavafxkteam;

import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.chart.LineChart;
import javafx.scene.chart.XYChart;

import java.net.URL;
import java.util.ResourceBundle;

public class Controller20 implements Initializable {
    @FXML
    LineChart<String, Number> lineChart;


    @Override
    public void initialize(URL url, ResourceBundle resourceBundle) {
        XYChart.Series<String, Number> series = new XYChart.Series<>();
        XYChart.Data<String, Number> jan = new XYChart.Data<>("Jan", 300);
        XYChart.Data<String, Number> feb = new XYChart.Data<>("feb", 400);
        XYChart.Data<String, Number> mar = new XYChart.Data<>("mar", 550);
        XYChart.Data<String, Number> apr = new XYChart.Data<>("apr", 750);
        XYChart.Data<String, Number> may = new XYChart.Data<>("may", 100);
        series.getData().addAll(jan, feb, mar, apr, may);
        series.setName("Salary per month of An");
        lineChart.getData().add(series);

        XYChart.Series<String, Number> series1 = new XYChart.Series<>();
        XYChart.Data<String, Number> jan1 = new XYChart.Data<>("Jan", 100);
        XYChart.Data<String, Number> feb1 = new XYChart.Data<>("feb", 490);
        XYChart.Data<String, Number> mar1 = new XYChart.Data<>("mar", 150);
        XYChart.Data<String, Number> apr1 = new XYChart.Data<>("apr", 950);
        XYChart.Data<String, Number> may1 = new XYChart.Data<>("may", 100);
        series1.getData().addAll(jan1, feb1, mar1, apr1, may1);
        series1.setName("Salary per month of Minh");
        lineChart.getData().add(series1);
    }
}
