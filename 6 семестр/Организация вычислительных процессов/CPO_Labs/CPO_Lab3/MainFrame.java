import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;

public class MainFrame extends JFrame {

    private JTabbedPane tabbedPane;

    public MainFrame() {
        super();
        setTitle("Лабораторна робота №3 - Алгоритм Корбато");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setMinimumSize(new Dimension(800, 600));
        setExtendedState(JFrame.MAXIMIZED_BOTH);
        tabbedPane = new JTabbedPane();
        JPanel vPanel = new VisualizationPanel();
        WaitTimePanel g1Panel = new WaitTimePanel();
        CPUDowntimePanel g2Panel = new CPUDowntimePanel();
        PriorityPanel g3Panel = new PriorityPanel();
        tabbedPane.add("Потактова візуалізація", vPanel);
        tabbedPane.add("Графік залежності середнього часу очікування від інтенсивності", g1Panel);
        tabbedPane.add("Графік залежності проценту простою ресурсу від  інтенсивності", g2Panel);
        tabbedPane.add("Графік залежності середнього часу очікування від  пріоритету", g3Panel);
        tabbedPane.setSelectedIndex(0);
        add(tabbedPane);
    }

    private class VisualizationPanel extends JPanel {

        private JTextField lambdaField;
        private JTextField minLpField;
        private JTextField maxLpField;
        private JTextField tkField;
        private JTextField ltkField;
        private JTextField queuesCountField;
        private JTextField stepsField;
        private JTextArea consoleArea;
        private JButton clearButton;

        private Corbato corbato;
        private int step;

        public VisualizationPanel() {
            super();
            setLayout(new BorderLayout());
            JPanel parametersPanel = new JPanel();
            parametersPanel.setLayout(new GridLayout(8, 1));
            JPanel tempPanel = new JPanel();
            tempPanel.setLayout(new FlowLayout(FlowLayout.RIGHT));
            tempPanel.add(new JLabel("Інтенсивність вхідного потоку заявок"));
            lambdaField = new JTextField();
            lambdaField.setColumns(10);
            tempPanel.add(lambdaField);
            parametersPanel.add(tempPanel);
            tempPanel = new JPanel();
            tempPanel.setLayout(new FlowLayout(FlowLayout.RIGHT));
            tempPanel.add(new JLabel("Мінімальна довжина програми"));
            minLpField = new JTextField();
            minLpField.setColumns(10);
            tempPanel.add(minLpField);
            parametersPanel.add(tempPanel);
            tempPanel = new JPanel();
            tempPanel.setLayout(new FlowLayout(FlowLayout.RIGHT));
            tempPanel.add(new JLabel("Максимальна довжина програми"));
            maxLpField = new JTextField();
            maxLpField.setColumns(10);
            tempPanel.add(maxLpField);
            parametersPanel.add(tempPanel);
            tempPanel = new JPanel();
            tempPanel.setLayout(new FlowLayout(FlowLayout.RIGHT));
            tempPanel.add(new JLabel("Час Tk"));
            tkField = new JTextField();
            tkField.setColumns(10);
            tempPanel.add(tkField);
            parametersPanel.add(tempPanel);
            tempPanel = new JPanel();
            tempPanel.setLayout(new FlowLayout(FlowLayout.RIGHT));
            tempPanel.add(new JLabel("Кількість байт за час Tk"));
            ltkField = new JTextField();
            ltkField.setColumns(10);
            tempPanel.add(ltkField);
            parametersPanel.add(tempPanel);
            tempPanel = new JPanel();
            tempPanel.setLayout(new FlowLayout(FlowLayout.RIGHT));
            tempPanel.add(new JLabel("Кількість черг"));
            queuesCountField = new JTextField();
            queuesCountField.setColumns(10);
            tempPanel.add(queuesCountField);
            parametersPanel.add(tempPanel);
            tempPanel = new JPanel();
            tempPanel.setLayout(new FlowLayout(FlowLayout.RIGHT));
            tempPanel.add(new JLabel("Кількість тактів при моделюванні"));
            stepsField = new JTextField();
            stepsField.setColumns(10);
            tempPanel.add(stepsField);
            parametersPanel.add(tempPanel);
            tempPanel = new JPanel();
            tempPanel.setLayout(new FlowLayout(FlowLayout.RIGHT));
            clearButton = new JButton(new AbstractAction() {
                public void actionPerformed(ActionEvent event) {
                    lambdaField.setEnabled(true);
                    minLpField.setEnabled(true);
                    maxLpField.setEnabled(true);
                    tkField.setEnabled(true);
                    ltkField.setEnabled(true);
                    queuesCountField.setEnabled(true);
                    consoleArea.setText("");
                    ((JButton)event.getSource()).setEnabled(false);
                    corbato = null;
                }
            });
            clearButton.setText("Зупинити");
            clearButton.setEnabled(false);
            tempPanel.add(clearButton);
            JButton stepButton = new JButton(new AbstractAction() {
                public void actionPerformed(ActionEvent event) {
                    if (corbato == null) {
                        lambdaField.setEnabled(false);
                        minLpField.setEnabled(false);
                        maxLpField.setEnabled(false);
                        tkField.setEnabled(false);
                        ltkField.setEnabled(false);
                        queuesCountField.setEnabled(false);
                        clearButton.setEnabled(true);
                        step = 0;
                        corbato = new Corbato(
                                Integer.valueOf(queuesCountField.getText()),
                                Integer.valueOf(tkField.getText()),
                                Integer.valueOf(ltkField.getText()),
                                Double.valueOf(lambdaField.getText()),
                                Integer.valueOf(minLpField.getText()),
                                Integer.valueOf(maxLpField.getText()));
                    }
                    consoleArea.setText(consoleArea.getText() + "Такт " +
                            String.valueOf(step + 1) + ":\n" + corbato.tactWithLog() + "\n");
                    step++;
                }
            });
            stepButton.setText("Такт");
            tempPanel.add(stepButton);
            JButton modellingButton = new JButton(new AbstractAction() {
                public void actionPerformed(ActionEvent event) {
                    if (corbato == null) {
                        lambdaField.setEnabled(false);
                        minLpField.setEnabled(false);
                        maxLpField.setEnabled(false);
                        tkField.setEnabled(false);
                        ltkField.setEnabled(false);
                        queuesCountField.setEnabled(false);
                        clearButton.setEnabled(true);
                        step = 0;
                        corbato = new Corbato(
                                Integer.valueOf(queuesCountField.getText()),
                                Integer.valueOf(tkField.getText()),
                                Integer.valueOf(ltkField.getText()),
                                Double.valueOf(lambdaField.getText()),
                                Integer.valueOf(minLpField.getText()),
                                Integer.valueOf(maxLpField.getText()));
                    }
                    int prevStep = step;
                    for (step = step; step < (prevStep + Integer.valueOf(stepsField.getText())); step++) {
                        consoleArea.setText(consoleArea.getText() + "Такт " +
                                String.valueOf(step + 1) + ":\n" + corbato.tactWithLog() + "\n");
                    }
                }
            });
            modellingButton.setText("Моделювання");
            tempPanel.add(modellingButton);
            parametersPanel.add(tempPanel);
            add(parametersPanel, BorderLayout.WEST);
            consoleArea = new JTextArea();
            consoleArea.setBackground(Color.WHITE);
            Font consoleFont = new Font("Monospaced", Font.PLAIN, 14);
            consoleArea.setEditable(false);
            consoleArea.setAutoscrolls(true);
            consoleArea.setFont(consoleFont);
            consoleArea.setForeground(Color.BLACK);
            JScrollPane consolePane = new JScrollPane(consoleArea);
            add(consolePane);
            corbato = null;
            step = 0;
        }

    }

    private class WaitTimePanel extends JPanel {

        private Corbato corbato;
        private GraphPanel graph;
        private JTextField maxLambdaField;
        private JTextField minLambdaField;
        private JTextField lambdaStepField;
        private JTextField stepCountField;

        public WaitTimePanel() {
            setLayout(new BorderLayout());
            JPanel optionsPanel = new JPanel();
            optionsPanel.setLayout(new GridLayout(5, 1));
            JPanel tempPanel = new JPanel();
            minLambdaField = new JTextField();
            minLambdaField.setColumns(10);
            tempPanel.add(new JLabel("Мінімальна інтенсивність вхідного потоку заявок"));
            tempPanel.add(minLambdaField);
            optionsPanel.add(tempPanel);
            tempPanel = new JPanel();
            maxLambdaField = new JTextField();
            maxLambdaField.setColumns(10);
            tempPanel.add(new JLabel("Максимальна інтенсивність вхідного потоку заявок"));
            tempPanel.add(maxLambdaField);
            optionsPanel.add(tempPanel);
            tempPanel = new JPanel();
            lambdaStepField = new JTextField();
            lambdaStepField.setColumns(10);
            tempPanel.add(new JLabel("Крок зміни інтенсивності"));
            tempPanel.add(lambdaStepField);
            optionsPanel.add(tempPanel);
            tempPanel = new JPanel();
            stepCountField = new JTextField();
            stepCountField.setColumns(10);
            tempPanel.add(new JLabel("Кількість кроків"));
            tempPanel.add(stepCountField);
            optionsPanel.add(tempPanel);
            JButton generateButton = new JButton();
            generateButton.setAction(new AbstractAction() {
                public void actionPerformed(ActionEvent event) {
                    double intensity = Double.valueOf(minLambdaField.getText());
                    graph.setModel(new GraphModel("Графік залежності середнього часу очікування від інтенсивності",
                            "Інтенсивність", "Середній час очікування"));
                    while (intensity <= Double.valueOf(maxLambdaField.getText())) {
                        corbato = new Corbato(10, 10, 100, intensity, 1, 10000);
                        for (int i = 0; i < Integer.valueOf(stepCountField.getText()); i++) {
                            corbato.tact();
                        }
                        graph.getModel().add(intensity, corbato.getAverageWaitTime());
                        intensity += Double.valueOf(lambdaStepField.getText());
                    }
                }
            });
            generateButton.setText("Побудувати");
            tempPanel = new JPanel();
            tempPanel.add(generateButton);
            optionsPanel.add(tempPanel);
            add(optionsPanel, BorderLayout.NORTH);
            graph = new GraphPanel();
            graph.setModel(new GraphModel("Графік залежності середнього часу очікування від інтенсивності",
                    "Інтенсивність", "Середній час очікування"));
            add(graph);
        }

    }

    private class CPUDowntimePanel extends JPanel {

        private Corbato corbato;
        private GraphPanel graph;
        private JTextField maxLambdaField;
        private JTextField minLambdaField;
        private JTextField lambdaStepField;
        private JTextField stepCountField;

        public CPUDowntimePanel() {
            setLayout(new BorderLayout());
            JPanel optionsPanel = new JPanel();
            optionsPanel.setLayout(new GridLayout(5, 1));
            JPanel tempPanel = new JPanel();
            minLambdaField = new JTextField();
            minLambdaField.setColumns(10);
            tempPanel.add(new JLabel("Мінимальна інтенсивність вхідного потоку заявок"));
            tempPanel.add(minLambdaField);
            optionsPanel.add(tempPanel);
            tempPanel = new JPanel();
            maxLambdaField = new JTextField();
            maxLambdaField.setColumns(10);
            tempPanel.add(new JLabel("Максимальна інтенсивність вхідного потоку заявок"));
            tempPanel.add(maxLambdaField);
            optionsPanel.add(tempPanel);
            tempPanel = new JPanel();
            lambdaStepField = new JTextField();
            lambdaStepField.setColumns(10);
            tempPanel.add(new JLabel("Крок зміни інтенсивності"));
            tempPanel.add(lambdaStepField);
            optionsPanel.add(tempPanel);
            tempPanel = new JPanel();
            stepCountField = new JTextField();
            stepCountField.setColumns(10);
            tempPanel.add(new JLabel("Кількість кроків"));
            tempPanel.add(stepCountField);
            optionsPanel.add(tempPanel);
            JButton generateButton = new JButton();
            generateButton.setAction(new AbstractAction() {
                public void actionPerformed(ActionEvent event) {
                    double intensity = Double.valueOf(minLambdaField.getText());
                    graph.setModel(new GraphModel("Графік залежності проценту простою ресурсу від  інтенсивності",
                            "Інтенсивніть", "Процент простою ресурсу"));
                    while (intensity <= Double.valueOf(maxLambdaField.getText())) {
                        corbato = new Corbato(10, 10, 100, intensity, 1, 10000);
                        for (int i = 0; i < Integer.valueOf(stepCountField.getText()); i++) {
                            corbato.tact();
                        }
                        graph.getModel().add(intensity, corbato.getCPUdowntimePercent());
                        intensity += Double.valueOf(lambdaStepField.getText());
                    }
                }
            });
            generateButton.setText("Побудувати");
            tempPanel = new JPanel();
            tempPanel.add(generateButton);
            optionsPanel.add(tempPanel);
            add(optionsPanel, BorderLayout.NORTH);
            graph = new GraphPanel();
            graph.setModel(new GraphModel("Графік залежності проценту простою ресурсу від  інтенсивності",
                    "Інтенсивніть", "Процент простою ресурсу"));
            add(graph);
        }

    }

    private class PriorityPanel extends JPanel {

        private Corbato corbato;
        private GraphPanel graph;
        private JTextField lambdaField;
        private JTextField stepCountField;

        public PriorityPanel() {
            setLayout(new BorderLayout());
            JPanel optionsPanel = new JPanel();
            optionsPanel.setLayout(new GridLayout(3, 1));
            JPanel tempPanel = new JPanel();
            lambdaField = new JTextField();
            lambdaField.setColumns(10);
            tempPanel.add(new JLabel("Інтенсивність вхідного потоку заявок"));
            tempPanel.add(lambdaField);
            optionsPanel.add(tempPanel);
            tempPanel = new JPanel();
            stepCountField = new JTextField();
            stepCountField.setColumns(10);
            tempPanel.add(new JLabel("Кількість кроків"));
            tempPanel.add(stepCountField);
            optionsPanel.add(tempPanel);
            JButton generateButton = new JButton();
            generateButton.setAction(new AbstractAction() {
                public void actionPerformed(ActionEvent event) {
                    double intensity = Double.valueOf(lambdaField.getText());
                    graph.setModel(new GraphModel("Графік залежності середнього часу очікування від  пріоритету",
                            "Пріоритет заявки", "Середній час очікування"));
                    for (int priority = 1; priority < 10000; priority++) {
                        corbato = new Corbato(10, 10, 100, intensity, priority, priority);
                        for (int i = 0; i < Integer.valueOf(stepCountField.getText()); i++) {
                            corbato.tact();
                        }
                        graph.getModel().add(priority, corbato.getAverageWaitTime());
                    }
                }
            });
            generateButton.setText("Побудувати");
            tempPanel = new JPanel();
            tempPanel.add(generateButton);
            optionsPanel.add(tempPanel);
            add(optionsPanel, BorderLayout.NORTH);
            graph = new GraphPanel();
            graph.setModel(new GraphModel("Графік залежності середнього часу очікування від  пріоритету",
                    "Пріоритет заявки", "Середній час очікування"));
            add(graph);
        }

    }

}
