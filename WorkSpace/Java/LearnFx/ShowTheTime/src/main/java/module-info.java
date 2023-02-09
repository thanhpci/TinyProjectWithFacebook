module com.example.showthetime {
    requires javafx.controls;
    requires javafx.fxml;
    requires javafx.graphics;


    opens com.example.showthetime to javafx.fxml;
    exports com.example.showthetime;
}