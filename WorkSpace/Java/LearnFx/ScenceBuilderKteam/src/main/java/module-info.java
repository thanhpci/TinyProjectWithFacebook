module com.example.scencebuilderkteam {
    requires javafx.controls;
    requires javafx.fxml;


    opens com.example.scencebuilderkteam to javafx.fxml;
    exports com.example.scencebuilderkteam;
}