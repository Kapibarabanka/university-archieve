import java.util.ArrayList;

public class ProgramQueue {

    private ArrayList<Program> programs;

    public ProgramQueue() {
        programs = new ArrayList<Program>();
    }

    public int getSize() {
        return programs.size();
    }

    public void add(Program p) {
        programs.add(p);
    }

    public Program get(int i) {
        return programs.get(i);
    }

    public void waitAll(int tk) {
        if (programs.size() > 0) {
            for (Program p : programs) {
                p.wait(tk);
            }
        }
    }

    public Program waitAllExcept(int e, int tk, int ltk) {
        Program program = null;
        for (int i = 0; i < programs.size(); i++) {
            if (i != e) {
                programs.get(i).wait(tk);
            }
            else {
                programs.get(i).execute(ltk);
                program = programs.get(i).copy();
                programs.remove(i);
            }
        }
        return program;
    }

}
