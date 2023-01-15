package neoMaPy.ui.graphstream;

import java.awt.BorderLayout;
import java.awt.Component;
import java.awt.event.MouseWheelEvent;
import java.awt.event.MouseWheelListener;

import javax.swing.JPanel;

import org.graphstream.ui.geom.Point2;
import org.graphstream.ui.geom.Point3;
import org.graphstream.ui.swing.SwingGraphRenderer;
import org.graphstream.ui.swing_viewer.DefaultView;
import org.graphstream.ui.swing_viewer.SwingViewer;
import org.graphstream.ui.swing_viewer.util.DefaultMouseManager;
import org.graphstream.ui.view.View;
import org.graphstream.ui.view.Viewer;
import org.graphstream.ui.view.camera.Camera;

import neoMaPy.NeoMaPy;

public class GraphStreamPanel extends JPanel {
	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;

	// CSS :
	// https://graphstream-project.org/doc/Advanced-Concepts/GraphStream-CSS-Reference/

	int width, height;
	Viewer viewer;
	RightPanel rp;

	private NeoMaPyGraph graph;
	private DefaultMouseManager mouseManager;

	public GraphStreamPanel(int width, int height) {
		super();
		this.width= width;
		this.height = height;
	}

	public void initGraph () {
		graph = new NeoMaPyGraph("NeoMaPy");
		viewer = new SwingViewer(graph, SwingViewer.ThreadingModel.GRAPH_IN_ANOTHER_THREAD);
		graph.setAttribute("ui.stylesheet", "url('file://conf/NeoMaPy.css')");
		NeoMaPy.loadGraph();
		
		doLayout();
		viewer();
		// graph.setAttribute("ui.stylesheet", cssStyle);
	}
	
	public void viewer() {
		setLayout(new BorderLayout());

		viewer.enableAutoLayout();
		add((DefaultView) viewer.addView("NeoMaPy", new SwingGraphRenderer()), BorderLayout.CENTER);

		//add(new ButtonPanel(this), BorderLayout.NORTH);
		add(rp = new RightPanel(graph, width, height), BorderLayout.EAST);
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

	public Viewer getViewer () {
		return viewer;
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
