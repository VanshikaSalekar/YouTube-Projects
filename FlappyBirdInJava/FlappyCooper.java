import javafx.animation.AnimationTimer;
import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.image.Image;
import javafx.scene.layout.StackPane;
import javafx.scene.paint.Color;
import javafx.stage.Stage;

public class FlappyCooper extends Application {
    private double birdY = 300;
    private double birdVelocity = 0;
    private final double GRAVITY = 0.4;
    private final double FLAP = -8;
    private boolean gameActive = true;

    @Override
    public void start(Stage stage) {
        Canvas canvas = new Canvas(400, 600);
        GraphicsContext gc = canvas.getGraphicsContext2D();

        Image bird = new Image("bird.png");
        Image background = new Image("background.png");

        // Game loop
        AnimationTimer timer = new AnimationTimer() {
            @Override
            public void handle(long now) {
                if (gameActive) {
                    birdVelocity += GRAVITY;
                    birdY += birdVelocity;

                    // Draw background and bird
                    gc.drawImage(background, 0, 0);
                    gc.drawImage(bird, 100, birdY);

                    // Collision check
                    if (birdY >= 600 || birdY <= 0) {
                        gameActive = false;
                    }
                } else {
                    gc.setFill(Color.RED);
                    gc.fillText("Game Over", 150, 300);
                }
            }
        };

        timer.start();

        Scene scene = new Scene(new StackPane(canvas), 400, 600);
        stage.setScene(scene);
        stage.show();

        // Input handling
        scene.setOnKeyPressed(e -> {
            if (gameActive && e.getCode().toString().equals("SPACE")) {
                birdVelocity = FLAP;
            }
        });
    }

    public static void main(String[] args) {
        launch(args);
    }
}
