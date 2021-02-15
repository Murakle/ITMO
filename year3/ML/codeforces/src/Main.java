
import java.io.*;
import java.util.*;

public class Main {

    BufferedReader br;
    StringTokenizer in;
    PrintWriter pw;

    public void solve() throws IOException {
        int k1 = nextInt();
        int k2 = nextInt();
        int n = nextInt();
        HashMap<Integer, Integer>[] m1 = new HashMap[k1];
        for (int i = 0; i < k1; i++) {
            m1[i] = new HashMap<>();
        }
        double[] sum1 = new double[k1];
        for (int i = 0; i < n; i++) {
            int x1 = nextInt() - 1;
            int x2 = nextInt() - 1;
            if (!m1[x1].containsKey(x2)) {
                m1[x1].put(x2, 0);
            }
            m1[x1].put(x2, m1[x1].get(x2) + 1);
            sum1[x1]++;
        }
        double res = 0;
        for (int i = 0; i < k1; i++) {
            for (HashMap.Entry<Integer, Integer> entry :
                    m1[i].entrySet()) {
                res += (double) entry.getValue() / n * Math.log((double) entry.getValue() / sum1[i]);
            }
        }
        pw.print(-res);
    }

    public class Pair implements Comparable<Pair> {
        long x;
        long y;

        public Pair(long x, long y) {
            this.x = x;
            this.y = y;
        }


        @Override
        public int compareTo(Pair o) {
            if (x != o.x) {
                return Long.compare(x, o.x);
            }
            return Long.compare(y, o.y);
        }
    }

    public void run() {
        try {
//            br = new BufferedReader(new FileReader("maxflow.in"));
//            pw = new PrintWriter(new FileWriter("maxflow.out"));
            br = new BufferedReader(new InputStreamReader(System.in));
            pw = new PrintWriter(new OutputStreamWriter(System.out));
//            br = new BufferedReader(new FileReader("/Users/user/dev/ITMO/year3/ML/codeforces/input.txt"));
//            pw = new PrintWriter(new FileWriter("/Users/user/dev/ITMO/year3/ML/codeforces/output.txt"));
            solve();
            pw.close();
        } catch (IOException e) {
            e.printStackTrace();
            System.exit(1);
        }
    }

    public String nextToken() throws IOException {
        while (in == null || !in.hasMoreTokens()) {
            in = new StringTokenizer(br.readLine());
        }
        return in.nextToken();
    }

    public int nextInt() throws IOException {
        return Integer.parseInt(nextToken());
    }

    public long nextLong() throws IOException {
        return Long.parseLong(nextToken());
    }

    public double nextDouble() throws IOException {
        return Double.parseDouble(nextToken());
    }


    public static void main(String[] args) throws IOException {
        Locale.setDefault(Locale.US);
        new Main().run();
    }
}
