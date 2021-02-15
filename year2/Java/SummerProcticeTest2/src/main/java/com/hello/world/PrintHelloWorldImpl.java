package com.hello.world;

public class PrintHelloWorldImpl implements IPrintHelloWorld {
    @Override
    public void print() {
        System.out.println("Hello OSGi World!");
    }
}
