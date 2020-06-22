public class Program {

    private int startLp;
    private int lp;
    private int waitTime;

    public Program(int lp) {
        this.lp = lp;
        startLp = lp;
        waitTime = 0;
    }

    public static Program generateProgram(int minLp, int maxLp) {
        return new Program(minLp + (int)(Math.random() * (double)(maxLp - minLp)));
    }

    public Program copy() {
        Program copyProgram = new Program(this.lp);
        copyProgram.waitTime = this.waitTime;
        copyProgram.startLp = startLp;
        return copyProgram;
    }

    public int getStartLp() {
        return startLp;
    }

    public int getLp() {
        return lp;
    }

    public void execute(int ltk) {
        lp -= ltk;
    }

    public void wait(int tk) {
        waitTime += tk;
    }

    public int getWaitTime() {
        return waitTime;
    }

}
