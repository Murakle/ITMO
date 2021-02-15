
import java.io.*;
import java.util.*;

public class Generate {

    BufferedReader br;
    StringTokenizer in;
    PrintWriter pw;
    int k;

    public void solve() throws IOException {
        Random r = new Random();
        k = r.nextInt(4) + 1;
        pw.println(k);
        for (int i = 0; i < k; i++) {
            int h = r.nextInt(10) + 1;
            pw.print(h + " ");
        }
        pw.println();

        pw.println(r.nextInt(10) + 1); // a
        int n = r.nextInt(4) + 3;
        pw.println(n); // n
        int wordlist = r.nextInt(5) + 2;
        for (int i = 0; i < n; i++) {
            int c = r.nextInt(k) + 1;
            pw.print(c + " ");
            int l = r.nextInt(6) + 1;
            pw.print(l + " ");
            for (int j = 0; j < l; j++) {
                int w = r.nextInt(wordlist);
                pw.print(w + " ");
            }
            pw.println();
        }
        int m = r.nextInt(4) + 3;
        pw.println(m); // m
        int test_wordlist = r.nextInt(4) + 3;
        for (int i = 0; i < m; i++) {
            int l = r.nextInt(6) + 1;
            pw.print(l + " ");
            for (int j = 0; j < l; j++) {
                int w = r.nextInt(test_wordlist);
                pw.print(w + " ");
            }
            pw.println();
        }
    }


    public void run() {
        try {
//            br = new BufferedReader(new FileReader("maxflow.in"));
//            pw = new PrintWriter(new FileWriter("maxflow.out"));
//            br = new BufferedReader(new InputStreamReader(System.in));
//            pw = new PrintWriter(new OutputStreamWriter(System.out));
//            br = new BufferedReader(new FileReader("input.txt"));
            pw = new PrintWriter(new FileWriter("/Users/user/dev/ITMO/year3/ML/codeforces/input.txt"));
            solve();
            pw.close();
        } catch (IOException e) {
            e.printStackTrace();
            System.exit(1);
        }
    }


    public static void main(String[] args) throws IOException {
        Locale.setDefault(Locale.US);
        new Generate().run();
    }
}
