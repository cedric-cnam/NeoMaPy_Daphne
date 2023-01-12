package neoMaPy.ui;

import java.awt.BorderLayout;
import java.awt.Component;
import java.awt.Dimension;
import java.awt.Toolkit;
import java.awt.event.MouseWheelEvent;
import java.awt.event.MouseWheelListener;

import javax.swing.JFrame;

import org.graphstream.ui.geom.Point2;
import org.graphstream.ui.geom.Point3;
import org.graphstream.ui.swing.SwingGraphRenderer;
import org.graphstream.ui.swing_viewer.DefaultView;
import org.graphstream.ui.swing_viewer.SwingViewer;
import org.graphstream.ui.swing_viewer.util.DefaultMouseManager;
import org.graphstream.ui.view.View;
import org.graphstream.ui.view.Viewer;
import org.graphstream.ui.view.camera.Camera;

public class GraphStream extends JFrame {
	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;

	// CSS :
	// https://graphstream-project.org/doc/Advanced-Concepts/GraphStream-CSS-Reference/

	Viewer viewer;
	RightPanel rp;

	private NeoMaPyGraph graph;
	private DefaultMouseManager mouseManager;

	public GraphStream() {
		super();
		graph = new NeoMaPyGraph("NeoMaPy");
		viewer = new SwingViewer(graph, SwingViewer.ThreadingModel.GRAPH_IN_ANOTHER_THREAD);
		graph.setAttribute("ui.stylesheet", "url('file://conf/NeoMaPy.css')");
		// graph.setAttribute("ui.stylesheet", cssStyle);
	}

	public void viewer() {
		setLayout(new BorderLayout());
		Dimension screenSize = Toolkit.getDefaultToolkit().getScreenSize();
		int width = new Double(screenSize.getWidth()).intValue();
		int height = new Double(screenSize.getHeight()).intValue();
		setSize(width, height);
		viewer.enableAutoLayout();
		add((DefaultView) viewer.addView("NeoMaPy", new SwingGraphRenderer()), BorderLayout.CENTER);

		//add(new ButtonPanel(this), BorderLayout.NORTH);
		add(rp = new RightPanel(graph, width, height), BorderLayout.EAST);
		this.setJMenuBar(new MenuBar (this));

		setLocationRelativeTo(null);
		setVisible(true);

		mouseManager = new NeoMaPyMouseManager(this);
		// viewer.getView("NeoMaPy").enableMouseOptions();
		viewer.getView("NeoMaPy").setMouseManager(mouseManager);
		View view = viewer.getView("NeoMaPy");
		view.getCamera().setViewPercent(1);
		((Component) view).addMouseWheelListener(new MouseWheelListener() {
		    @Override
		    public void mouseWheelMoved(MouseWheelEvent e) {
		        e.consume();
		        int i = e.getWheelRotation();
		        double factor = Math.pow(1.25, i);
		        Camera cam = view.getCamera();
		        double zoom = cam.getViewPercent() * factor;
		        Point2 pxCenter  = cam.transformGuToPx(cam.getViewCenter().x, cam.getViewCenter().y, 0);
		        Point3 guClicked = cam.transformPxToGu(e.getX(), e.getY());
		        double newRatioPx2Gu = cam.getMetrics().ratioPx2Gu/factor;
		        double x = guClicked.x + (pxCenter.x - e.getX())/newRatioPx2Gu;
		        double y = guClicked.y - (pxCenter.y - e.getY())/newRatioPx2Gu;
		        cam.setViewCenter(x, y, 0);
		        cam.setViewPercent(zoom);
		    }
		});

		rp.setGraphInfo();

		// graph.countAttributes ();
		/*
		 * viewer = new SwingViewer(graph,
		 * Viewer.ThreadingModel.GRAPH_IN_ANOTHER_THREAD); viewer.addDefaultView(false);
		 * viewer.enableAutoLayout();
		 * 
		 * View view = viewer.getDefaultView(); mouseManager = new
		 * DefaultMouseManager(); view.setMouseManager(mouseManager);
		 * 
		 * this.add((ViewPanel)view);
		 */
	}

	public NeoMaPyGraph getGraph() {
		return graph;
	}

	void setInfo(String nodeId) {
		rp.setNodeInfo(nodeId);
	}

	public void cleanup() {
		if (viewer != null) {
			try {
				viewer.close();
			} catch (Throwable t) {
				System.out.println(t.getMessage() + " from closing GS-viewer.");
			}
		}
		for (Component c : this.getComponents()) {
			this.remove(c);
		}
		this.repaint();
		this.revalidate();
	}

	public String toString() {
		return "Graph (#nodes:" + graph.getNodeCount() + ",#edges:" + graph.getEdgeCount() + ")";// +graph.edgeAttributes;

	}
}
