module com.example.demojavafxkteam {
    requires javafx.controls;
    requires javafx.fxml;
    requires javafx.graphics;


    opens com.example.demojavafxkteam to javafx.fxml;
    exports com.example.demojavafxkteam;
}