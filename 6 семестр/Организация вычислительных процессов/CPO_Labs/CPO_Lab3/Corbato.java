import java.util.ArrayList;

public class Corbato {

    private int tk;
    private int ltk;
    private ArrayList<ProgramQueue> queues;
    private double lambda;
    private int minLp;
    private int maxLp;
    private int t;
    private int generateCount;
    private double averageWaitTime;
    private double sumWaitTime;
    private int doneCount;
    private int CPUdowntime;

    public Corbato(int queuesCount, int tk, int ltk, double lambda, int minLp, int maxLp) {
        queues = new ArrayList<ProgramQueue>();
        for (int i = 0; i < queuesCount; i++) {
            queues.add(new ProgramQueue());
        }
        this.tk = tk;
        this.ltk = ltk;
        this.lambda = lambda;
        this.minLp = minLp;
        this.maxLp = maxLp;
        t = 0;
        generateCount = 0;
        doneCount = 0;
        averageWaitTime = 0;
        sumWaitTime = 0;
        CPUdowntime = 0;
    }

    public double getAverageWaitTime() {
        return averageWaitTime;
    }

    public double getCPUdowntimePercent() {
        return ((double) CPUdowntime / (double) t);
    }

    public void addProgram(Program p) {
        int i = (int) (Math.log((double) p.getLp() / ltk) / Math.log(2));
        if (++i >= queues.size()) {
            i = queues.size() - 1;
        }
        if (i < 0) {
            i = 0;
        }
        queues.get(i).add(p);
    }

    public void tact() {
        int i = 0;
        while (((double) t * lambda) > generateCount) {
            Program p = Program.generateProgram(minLp, maxLp);
            addProgram(p);
            generateCount++;
        }
        while ((i < queues.size()) && (queues.get(i).getSize() == 0)) {
            i++;
        }
        boolean isResourceInUse = false;
        Program program = null;
        if (i < queues.size()) {
            for (int j = 0; j < queues.size(); j++) {
                if (j != i) {
                    queues.get(j).waitAll((int) (Math.pow(2, (double) i) * tk));
                }
            }
            program = queues.get(i).waitAllExcept(0, (int) (Math.pow(2, (double) i) * tk),
                    (int) (Math.pow(2, (double) i) * ltk));
            if (program.getLp() <= 0) {
                sumWaitTime += program.getWaitTime();
                averageWaitTime = sumWaitTime / ++doneCount;
            }
            if (program.getLp() >= 0) {
                if ((i + 1) < queues.size()) {
                    queues.get(i + 1).add(program);
                }
                else {
                    queues.get(i).add(program);
                }
                isResourceInUse = true;
            }
            else {
                isResourceInUse = false;
            }
        }
        if (isResourceInUse) {
            t += (int) (Math.pow(2, (double) i) * tk);
        }
        else {
            if (program == null) {
                t += tk;
                CPUdowntime += tk;
            }
            else {
                t += (int) (Math.pow(2, (double) i) * tk);
                CPUdowntime += ((double) Math.abs(program.getLp()) / ltk) * tk;
            }
        }
    }

    public String tactWithLog() {
        String log = "";
        int i = 0;
        while (((double) t * lambda) > generateCount) {
            Program p = Program.generateProgram(minLp, maxLp);
            addProgram(p);
            generateCount++;
            log += "Додана програма з довжиною Lp = " + String.valueOf(p.getLp()) + "\n";
        }
        while ((i < queues.size()) && (queues.get(i).getSize() == 0)) {
            i++;
        }
        boolean isResourceInUse = false;
        Program program = null;
        if (i < queues.size()) {
            for (int j = 0; j < queues.size(); j++) {
                if (j != i) {
                    queues.get(j).waitAll((int) (Math.pow(2, (double) i) * tk));
                }
            }
            log += "Виконання програми з черги №" + String.valueOf(i) + " с довжиною Lp = " +
                    String.valueOf(queues.get(i).get(0).getLp()) + " - " +
                    String.valueOf((int) (Math.pow(2, (double) i) * ltk));
            program = queues.get(i).waitAllExcept(0, (int) (Math.pow(2, (double) i) * tk),
                    (int) (Math.pow(2, (double) i) * ltk));
            if (program.getLp() <= 0) {
                sumWaitTime += program.getWaitTime();
                averageWaitTime = sumWaitTime / ++doneCount;
            }
            if (program.getLp() >= 0) {
                if ((i + 1) < queues.size()) {
                    queues.get(i + 1).add(program);
                    log += " = " + String.valueOf(program.getLp()) + "\n";
                }
                else {
                    queues.get(i).add(program);
                    log += " = " + String.valueOf(program.getLp()) + "\n";
                }
                isResourceInUse = true;
            }
            else {
                log += " = " + "0" + "\n";
                isResourceInUse = false;
            }
        }
        if (isResourceInUse) {
            t += (int) (Math.pow(2, (double) i) * tk);
            log += "Ресурс зайнятий\n";
        }
        else {
            log += "Ресурс вільний\n";
            if (program == null) {
                CPUdowntime += tk;
                t += tk;
            }
            else {
                CPUdowntime += ((double) Math.abs(program.getLp()) / ltk) * tk;
                t += (int) (Math.pow(2, (double) i) * tk);
            }
        }
        log += "Системний час: " + String.valueOf(t) + "\n";
        return log;
    }

}

