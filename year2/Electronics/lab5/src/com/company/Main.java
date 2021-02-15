package com.company;

import java.io.*;
import java.util.StringTokenizer;

public class Main {
    static BufferedReader br;
    static StringTokenizer in;

    public static void main(String[] args) throws IOException {

        PrintWriter pw = new PrintWriter(new OutputStreamWriter(System.out));
        br = new BufferedReader(new FileReader("data1.txt"));

        int n = 1000;
        double r[] = new double[n];
        double k[] = new double[n];
        for (int i = 0; i < n; i++) {
            r[i] = nextDouble();
            k[i] = nextDouble();
        }
        double minr = 0;
        double mink = 0;
        double maxr = 0;
        double maxk = 0;

        double N = 1.7d;
        double Rkr = 0.9992d;
        for (int i = 1; i < n - 1; i++) {
            if (k[i] > k[i - 1] && k[i] > k[i + 1]) {
                maxr = r[i];
                maxk = k[i];
                double R = (maxr + minr) / 2;
                double delta = R * R / Rkr * N;
                double V = (maxk - mink) / (maxk + mink);
                pw.println(V);
            }
            if (k[i] < k[i - 1] && k[i] < k[i + 1]) {
                minr = r[i];
                mink = k[i];
                double R = (maxr + minr) / 2;
                double delta = R * R / Rkr * N;  // 1e-6/1e-6 = 1
                double V = (maxk - mink) / (maxk + mink);
                pw.println(V);

            }
        }
        pw.close();
    }


    public static double nextDouble() {
        return Double.parseDouble(nextToken());
    }

    public static String nextToken() {
        while (in == null || !in.hasMoreTokens()) {
            try {
                in = new StringTokenizer(br.readLine());
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        return in.nextToken();
    }
}
