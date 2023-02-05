/**
 * Created by Nicolas Travers <nicolas.travers@devinci.fr> 2022-2023©
 */
package neoMaPy.ui.graphstream;

import java.awt.BorderLayout;
import java.awt.Component;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.awt.event.MouseWheelEvent;
import java.awt.event.MouseWheelListener;
import java.util.List;

import javax.swing.JPanel;

import org.graphstream.ui.geom.Point2;
import org.graphstream.ui.geom.Point3;
import org.graphstream.ui.graphicGraph.GraphicGraph;
import org.graphstream.ui.graphicGraph.GraphicNode;
import org.graphstream.ui.swing.SwingGraphRenderer;
import org.graphstream.ui.swing_viewer.DefaultView;
import org.graphstream.ui.swing_viewer.SwingViewer;
import org.graphstream.ui.swing_viewer.util.DefaultMouseManager;
import org.graphstream.ui.view.View;
import org.graphstream.ui.view.Viewer;
import org.graphstream.ui.view.camera.Camera;
import org.graphstream.ui.view.util.GraphMetrics;

import neoMaPy.NeoMaPy;
import neoMaPy.Query;
import neoMaPy.MaPyStrategy.MAPStrategy;
import neoMaPy.ui.NeoMaPyFrame;
import neoMaPy.ui.graphstream.info.RightPanel;

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

	public void initGraph (List<Query> queries) {
		if(graph !=null)
			return;
		graph = new NeoMaPyGraph("NeoMaPy");
		viewer = new SwingViewer(graph, SwingViewer.ThreadingModel.GRAPH_IN_ANOTHER_THREAD);
		graph.setAttribute("ui.stylesheet", "url('file://conf/NeoMaPy.css')");
		try {	// Allow time for the viewer to build
			Thread.sleep(500);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		NeoMaPy.loadGraph();
		try {	// Allow time for the viewer to build
			Thread.sleep(500);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		//doLayout();
		viewer(queries);
		// graph.setAttribute("ui.stylesheet", cssStyle);
	}
	
	public void viewer(List<Query> queries) {
		setLayout(new BorderLayout());

		viewer.enableAutoLayout();
		add((DefaultView) viewer.addView("NeoMaPy", new SwingGraphRenderer()), BorderLayout.CENTER);

		add(rp = new RightPanel(this, width, height), BorderLayout.EAST);
		//setVisible(true);

		mouseManager = new NeoMaPyMouseManager(this);
		// viewer.getView("NeoMaPy").enableMouseOptions();
		viewer.getView("NeoMaPy").setMouseManager(mouseManager);
		View view = viewer.getView("NeoMaPy");
		view.getCamera().setViewPercent(1);
		try {	// Allow time for the viewer to build
			Thread.sleep(500);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		((Component) view).addMouseWheelListener(new MouseWheelListener() {
		    @Override
		    public void mouseWheelMoved(MouseWheelEvent e) {
		        e.consume();
		        int i = e.getWheelRotation();
		        if(i == 0)
		        	return;
		        double factor = Math.pow(1.1, i);
		        Camera cam = view.getCamera();
		        double zoom = cam.getViewPercent() * factor;
		        if(zoom>2)
		        	return;
		        Point2 pxCenter  = cam.transformGuToPx(cam.getViewCenter().x, cam.getViewCenter().y, 0);
		        Point3 guClicked = cam.transformPxToGu(e.getX(), e.getY());
		        double newRatioPx2Gu = cam.getMetrics().ratioPx2Gu/factor;
		        double x = guClicked.x + (pxCenter.x - e.getX())/newRatioPx2Gu;
		        double y = guClicked.y - (pxCenter.y - e.getY())/newRatioPx2Gu;
		        cam.setViewCenter(x, y, 0);
		        cam.setViewPercent(zoom);
		    }
		});
		((Component) view).addMouseListener(new MouseListener () {
			double x, y;
			@Override
			public void mouseClicked(MouseEvent e) {}

			@Override
			public void mousePressed(MouseEvent e) {
				e.consume();
				x = e.getX();
				y = e.getY();
			}

			@Override
			public void mouseReleased(MouseEvent e) {
				e.consume();

				double height = y - e.getY();
				double width = e.getX() - x;
				if(width < 50 || height < 50)
					return;

				Camera cam = view.getCamera();
		        Point3 px1 = cam.transformPxToGu(x, y);
		        Point3 px2 = cam.transformPxToGu(e.getX(), e.getY());
		        

				GraphMetrics gm = cam.getMetrics();
		        double widthZoom = gm.graphWidthGU()/(px2.x-px1.x);
		        double heightZoom = gm.graphHeightGU()/(px2.y-px1.y);
		        
		        double multi = Math.min(widthZoom, heightZoom)/2;

				double centerX = x + width/2;
				double centerY = y - height/2;
		        Point3 pxCenter = cam.transformPxToGu(centerX, centerY);

		        double zoom = cam.getViewPercent() / multi;

				cam.setViewCenter(pxCenter.x, pxCenter.y, 0);
				cam.setViewPercent(zoom);
			}

			@Override
			public void mouseEntered(MouseEvent e) {}

			@Override
			public void mouseExited(MouseEvent e) {}});

		rp.setGraphInfo(queries);
	}

	public void zoomOnNode (String nodeId) {
		GraphicGraph gg = viewer.getGraphicGraph();
		GraphicNode gn = (GraphicNode)gg.getNode(nodeId);
	
		Camera cam = viewer.getView("NeoMaPy").getCamera();
		cam.setViewCenter(gn.getX(), gn.getY(), 0);
        cam.setViewPercent(0.05);
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

	public void processMAP(MAPStrategy s, List<Query> queries) {
		if(graph == null)
			NeoMaPyFrame.error("No Knowledge Graph generated\\Please create it in the \"Conflict Graph\" menu.");
		else {
			graph.processMAP(s);
			rp.setGraphInfo(queries);
		}
	}

	public void resetMap(List<Query> queries) {
		if(graph == null)
			NeoMaPyFrame.error("No Knowledge Graph generated\\Please create it in the \"Conflict Graph\" menu.");
		else {
			graph.resetMap();
			rp.setGraphInfo(queries);
		}
	}
	public String toString() {
		return "Graph (#nodes:" + graph.getNodeCount() + ",#edges:" + graph.getEdgeCount() + ")";// +graph.edgeAttributes;

	}
}
