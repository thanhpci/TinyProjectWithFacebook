module com.example.spotify1 {
    requires javafx.controls;
    requires javafx.fxml;
    requires javafx.graphics;


    opens com.example.spotify1 to javafx.fxml;
    exports com.example.spotify1;
}