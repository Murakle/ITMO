
import java.io.*;
import java.util.*;

public class Main {

    BufferedReader br;
    StringTokenizer in;
    PrintWriter pw;
    int k;
    int[] h;
    int a;
    int n;
    int[] c_train;
    String[][] w_train;
    int m;
    String[][] w_test;
    HashMap<Integer, Integer> ProbOfClasses; // p(ci)

    public double LaplasP(int Nx, int All, int Nk) {
        return (double) (Nx + a) / (Nk + All);
    }

    public void solve() throws IOException {
        k = nextInt();
        h = new int[k];
        a = nextInt();
        n = nextInt();
        c_train = new int[n];
        w_train = new String[n][];
        ProbOfClasses = new HashMap<>();
        HashMap<Integer, HashMap<String, Integer>> joinedEvents = new HashMap<>();
        TreeSet<String> wordList = new TreeSet<>();
        for (int i = 0; i < n; i++) {
            c_train[i] = nextInt();
            addToMap(ProbOfClasses, c_train[i], 1);
            int l = nextInt();
            w_train[i] = new String[l];
            for (int j = 0; j < l; j++) {
                w_train[i][j] = nextToken();
                wordList.add(w_train[i][j]);
            }
            addToMap(joinedEvents, c_train[i], w_train[i]);
        }

        m = nextInt();
        w_test = new String[m][];

        for (int i = 0; i < m; i++) {
            int l = nextInt();
            w_test[i] = new String[l];
            for (int j = 0; j < l; j++) {
                w_test[i][j] = nextToken();
            }
            for (int j = 0; j < k; j++) {
                double p = (double) ProbOfClasses.get((j + 1)) / n;
                for (int o = 0; o < l; o++) {
                    double Laplas = LaplasP(joinedEvents.get(j + 1).get(w_test[i][o]), ProbOfClasses.get(j + 1), 2);
                    pw.print(Laplas + " ");
                    if (joinedEvents.get((j + 1)).containsKey(w_test[i][o])) {
                        p *= LaplasP(joinedEvents.get(j + 1).get(w_test[i][o]), ProbOfClasses.get(j + 1), 2);
                    } else {
                        p *= (1 - LaplasP(joinedEvents.get(j + 1).get(w_test[i][o]), ProbOfClasses.get(j + 1), 2));
                    }
                }
                pw.println();
            }
        }
    }


    public void addToMap(HashMap<Integer, HashMap<String, Integer>> map, int key, String[] val) {
        if (!map.containsKey(key)) {
            map.put(key, new HashMap<>());
        }
        for (String s : val) {
            addToMap(map.get(key), s, 1);
        }
    }

    public void addToMap(Map<Integer, Integer> map, int key, int val) {
        if (!map.containsKey(key)) {
            map.put(key, 0);
        }
        map.put(key, map.get(key) + val);
    }

    public void addToMap(Map<String, Integer> map, String key, int val) {
        if (!map.containsKey(key)) {
            map.put(key, 0);
        }
        map.put(key, map.get(key) + val);
    }

    public void run() {
        try {
//            br = new BufferedReader(new FileReader("maxflow.in"));
//            pw = new PrintWriter(new FileWriter("maxflow.out"));
            br = new BufferedReader(new InputStreamReader(System.in));
            pw = new PrintWriter(new OutputStreamWriter(System.out));
//            br = new BufferedReader(new FileReader("input.txt"));
//            pw = new PrintWriter(new FileWriter("output.txt"));
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
