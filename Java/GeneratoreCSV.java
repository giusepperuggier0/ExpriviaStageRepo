import java.io.FileWriter;
import java.io.IOException;
import java.util.Random;

public class GeneratoreCSV {

    private static  String LETTERE = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
    private static  Random random = new Random();

    public static void main(String[] args) throws IOException {
        String percorsoCartella = "C:\\Users\\Giuseppe\\Desktop\\Stage_exprivia\\Java\\Javaoutput_csv";
        int numeroFile = 7;
        int righe = 20;
        int colonne = 4;

        for (int i = 1; i <= numeroFile; i++) {
            String nomeFile = percorsoCartella + "/file_" + i + ".csv";
            boolean usaStringhe = random.nextBoolean();
            generaCSV(nomeFile, righe, colonne, usaStringhe);
        }
    }

    public static void generaCSV(String percorsoFile, int righe, int colonne, boolean usaStringhe) {
        try (FileWriter writer = new FileWriter(percorsoFile)) {
            for (int i = 0; i < righe; i++) {
                for (int j = 0; j < colonne; j++) {
                    writer.append(usaStringhe ? generaStringaCasuale(8) : String.valueOf(random.nextInt(1000)));
                    if (j < colonne - 1) writer.append(",");
                }
                writer.append("\n");
            }
        } catch (Exception ignored) {}
    }

    private static String generaStringaCasuale(int lunghezza) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < lunghezza; i++) {
            sb.append(LETTERE.charAt(random.nextInt(LETTERE.length())));
        }
        return sb.toString();
    }
}
