
import java.io.*;
import java.util.*;

public class Test {

    BufferedReader br1;
    StringTokenizer in1;
    BufferedReader br2;
    StringTokenizer in2;
    PrintWriter pw;


    public void solve() throws IOException {
        double eps = 1e-6;
        while (true) {
            String s1 = br1.readLine();
            String s2 = br2.readLine();

            if (s1 == null || s2 == null) {
                pw.print("Not Found");
                return;
            }
            String[] r1 = s1.split(" ");
            String[] r2 = s2.split(" ");
            for (int i = 0; i < r1.length; i++) {
                double n1 = Double.parseDouble(r1[i]);
                double n2 = Double.parseDouble(r2[i]);
                if (Math.abs(n1 - n2) > eps) {
                    pw.print("Found");
                    return;
                }
            }

        }
    }


    public void run() {
        try {
//            br = new BufferedReader(new FileReader("maxflow.in"));
//            pw = new PrintWriter(new FileWriter("maxflow.out"));
//            br = new BufferedReader(new InputStreamReader(System.in));
//            pw = new PrintWriter(new OutputStreamWriter(System.out));
            br1 = new BufferedReader(new FileReader("/Users/user/dev/ITMO/year3/ML/labs/lab3/output.txt"));
            br2 = new BufferedReader(new FileReader("/Users/user/dev/ITMO/year3/ML/codeforces/output.txt"));
            pw = new PrintWriter(new FileWriter("/Users/user/dev/ITMO/year3/ML/codeforces/src/result.txt"));
            solve();
            pw.close();
        } catch (IOException e) {
            e.printStackTrace();
            System.exit(1);
        }
    }

    public String nextToken(StringTokenizer in, BufferedReader br) throws IOException {
        while (in == null || !in.hasMoreTokens()) {
            in = new StringTokenizer(br.readLine());
        }
        return in.nextToken();
    }


    public static void main(String[] args) throws IOException {
        Locale.setDefault(Locale.US);
        new Test().run();
    }
}
