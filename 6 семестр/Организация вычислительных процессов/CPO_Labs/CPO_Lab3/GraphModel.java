import org.jfree.data.xy.XYSeries;
import org.jfree.data.xy.XYSeriesCollection;

import java.util.HashMap;

public class GraphModel {

    private String name;
    private String xName;
    private String yName;
    private XYSeries data;
    private HashMap<Double, Integer> xCount;

    public GraphModel(String name, String xName, String yName) {
        this.name = name;
        this.xName = xName;
        this.yName = yName;
        data = new XYSeries(this.name, true);
        xCount = new HashMap<Double, Integer>();
    }

    public String getName() {
        return name;
    }

    public String getXName() {
        return xName;
    }

    public String getYName() {
        return yName;
    }

    public XYSeriesCollection getDataset() {
        return new XYSeriesCollection(data);
    }

    public void removeAll() {
        data = new XYSeries(this.name, true);
        xCount = new HashMap<Double, Integer>();
    }

    public void add(double x, double y) {
        if (xCount.containsKey(Double.valueOf(x))) {
            int i = 0;
            while (data.getX(i).doubleValue() != x) {
                i++;
            }
            int prevCount = xCount.get(Double.valueOf(x));
            xCount.put(x, Integer.valueOf(++prevCount));
            double temp = data.getY(i).doubleValue();
            temp += y;
            temp /= xCount.get(Double.valueOf(x).doubleValue());
            data.remove(i);
            data.add(x, temp);
        }
        else {
            data.add(x, y);
            xCount.put(Double.valueOf(x), 1);
        }
    }

}
