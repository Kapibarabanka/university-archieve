import org.jfree.chart.ChartFactory;
import org.jfree.chart.ChartPanel;
import org.jfree.chart.JFreeChart;
import org.jfree.chart.plot.PlotOrientation;
import org.jfree.chart.plot.XYPlot;

import javax.swing.*;
import java.awt.*;

public class GraphPanel extends JPanel {

    private JFreeChart chart;
    private GraphModel model;

    public GraphPanel() {
        super();
    }

    public void setModel(GraphModel model) {
        this.model = model;
        refresh();
    }

    public GraphModel getModel() {
        return model;
    }

    public void refresh() {
        chart = ChartFactory.createXYLineChart(
                this.model.getName(),
                this.model.getXName(),
                this.model.getYName(),
                this.model.getDataset(),
                PlotOrientation.VERTICAL,
                false,
                false,
                false
        );
        XYPlot plot = chart.getXYPlot();
        plot.setBackgroundPaint(Color.WHITE);
        plot.setDomainGridlinePaint(Color.DARK_GRAY);
        plot.setRangeGridlinePaint(Color.DARK_GRAY);

        this.removeAll();
        add(new ChartPanel(chart));
        revalidate();
        repaint();
    }

}
