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
import java.util.EnumSet;
import java.util.List;

import javax.swing.JPanel;

import org.graphstream.ui.geom.Point2;
import org.graphstream.ui.geom.Point3;
import org.graphstream.ui.graphicGraph.GraphicElement;
import org.graphstream.ui.graphicGraph.GraphicGraph;
import org.graphstream.ui.graphicGraph.GraphicNode;
import org.graphstream.ui.swing.SwingGraphRenderer;
import org.graphstream.ui.swing_viewer.DefaultView;
import org.graphstream.ui.swing_viewer.SwingViewer;
import org.graphstream.ui.view.View;
import org.graphstream.ui.view.Viewer;
import org.graphstream.ui.view.ViewerListener;
import org.graphstream.ui.view.ViewerPipe;
import org.graphstream.ui.view.camera.Camera;
import org.graphstream.ui.view.util.GraphMetrics;
import org.graphstream.ui.view.util.InteractiveElement;

import neoMaPy.NeoMaPy;
import neoMaPy.Query;
import neoMaPy.MaPyStrategy.MAPStrategy;
import neoMaPy.ui.NeoMaPyFrame;
import neoMaPy.ui.graphstream.info.MAPBar;
import neoMaPy.ui.graphstream.info.RightPanel;

public class GraphStreamPanel extends JPanel implements ViewerListener {
	/**
	 * 
	 */
	protected static final long serialVersionUID = 1L;
	protected boolean loop = true;

	// CSS :
	// https://graphstream-project.org/doc/Advanced-Concepts/GraphStream-CSS-Reference/

	int width, height;
	Viewer viewer;
	RightPanel rp;

	private NeoMaPyGraph graph;

	public GraphStreamPanel(int width, int height) {
		super();
		//this.setSize(width, height);
		this.width = width;
		this.height = height;
	}

	public void initGraph(List<Query> queries) {
		if (graph != null)
			return;
		graph = new NeoMaPyGraph("NeoMaPy");
		viewer = new SwingViewer(graph, SwingViewer.ThreadingModel
				//.GRAPH_IN_GUI_THREAD);
				.GRAPH_IN_ANOTHER_THREAD);
		graph.setAttribute("ui.stylesheet", "url('file://conf/NeoMaPy.css')");
		try { // Allow time for the viewer to build
			Thread.sleep(500);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		NeoMaPy.loadGraph();
		try { // Allow time for the viewer to build
			Thread.sleep(500);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		// doLayout();
		viewer(queries);
		// graph.setAttribute("ui.stylesheet", cssStyle);
	}

	public void viewer(List<Query> queries) {
		setLayout(new BorderLayout());

		//TODO: addon viewer pipe
		
		viewer.setCloseFramePolicy(Viewer.CloseFramePolicy.HIDE_ONLY);
		ViewerPipe fromViewer = viewer.newViewerPipe();
		fromViewer.addViewerListener(this);
		fromViewer.addSink(graph);
		
		//while(loop) {
			fromViewer.pump(); // or fromViewer.blockingPump(); in the nightly builds

			// here your simulation code.

			// You do not necessarily need to use a loop, this is only an example.
			// as long as you call pump() before using the graph. pump() is non
			// blocking.  If you only use the loop to look at event, use blockingPump()
			// to avoid 100% CPU usage. The blockingPump() method is only available from
			// the nightly builds.
		//}
	
		//
		
		viewer.enableAutoLayout();
		add((DefaultView) viewer.addView("NeoMaPy", new SwingGraphRenderer()), BorderLayout.CENTER);

		add(rp = new RightPanel(this, width, height), BorderLayout.EAST);
		// setVisible(true);

		View view = viewer.getView("NeoMaPy");
		
		Camera cam = view.getCamera();
		cam.setAutoFitView(true);
		view.enableMouseOptions();
		//view.setMouseManager(mouseManager);
		//cam.setViewPercent(1);
		//cam.setBounds(0, 0, width, height, 0, 0);

		System.out.println(((Component)view).getBounds());
				
		GraphMetrics gm = cam.getMetrics();

		try { // Allow time for the viewer to build
			Thread.sleep(500);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}

		((Component) view).addMouseWheelListener(new MouseWheelListener() {
			@Override
			public void mouseWheelMoved(MouseWheelEvent e) {
				e.consume();
				int i = e.getWheelRotation();
				if (i == 0)
					return;
				double factor = Math.pow(1.1, i);
				double zoom = cam.getViewPercent() * factor;
				if (zoom > 1.1) {
					resetZoom();
					return;
				}
				if (zoom < 0.05)
					return;
				Point2 pxCenter = cam.transformGuToPx(cam.getViewCenter().x, cam.getViewCenter().y, 0);
				Point3 guClicked = cam.transformPxToGu(e.getX(), e.getY());
				double newRatioPx2Gu = cam.getMetrics().ratioPx2Gu / factor;
				double x = guClicked.x + (pxCenter.x - e.getX()) / newRatioPx2Gu;
				double y = guClicked.y - (pxCenter.y - e.getY()) / newRatioPx2Gu;
				System.out.println(x+"-"+y+" ("+zoom+")");
				cam.setViewCenter(x, y, 0);
				cam.setViewPercent(zoom);
			}
		});
		((Component) view).addMouseListener(new MouseListener() {
			double x, y;

			@Override
			public void mouseClicked(MouseEvent e) {
				try {
					GraphicElement ge = view.findGraphicElementAt(EnumSet.of(InteractiveElement.NODE), e.getX(), e.getY());
					if (ge != null) {
						setInfo(ge.getId());
					}
				} catch (Exception ex) {

				}
			}

			@Override
			public void mousePressed(MouseEvent e) {
				e.consume();
				x = e.getX();
				y = e.getY();
				//Point3 guClicked = cam.transformPxToGu(x, y);
				//Point3 pxClicked = cam.transformGuToPx(guClicked.x, guClicked.y, 0);
			}

			@Override
			public void mouseReleased(MouseEvent e) {
				e.consume();

				double height = y - e.getY();
				double width = e.getX() - x;
				if (width < 50 || height < 50)
					return;

				//viewer.replayGraph(graph);
				Point3 px1 = cam.transformPxToGu(x, y);
				Point3 px2 = cam.transformPxToGu(e.getX(), e.getY());

				double widthZoom = gm.graphWidthGU() / (px2.x - px1.x);
				double heightZoom = gm.graphHeightGU() / (px2.y - px1.y);

				double multi = Math.min(widthZoom, heightZoom) / 2;

				double centerX = x + width / 2;
				double centerY = y - height / 2;
				Point3 pxCenter = cam.transformPxToGu(centerX, centerY);

				double zoom = cam.getViewPercent() / multi;
				if (zoom > 1.5 || zoom < 0.05)
					return;

				cam.setViewCenter(pxCenter.x, pxCenter.y, 0);
				cam.setViewPercent(zoom);
				//cam.setBounds(0, 0, width, height, 0, 0);

			}

			@Override
			public void mouseEntered(MouseEvent e) {
			}

			@Override
			public void mouseExited(MouseEvent e) {
			}
		});

		rp.setGraphInfo(queries);
	}

	public void zoomOnNode(String nodeId) {
		GraphicGraph gg = viewer.getGraphicGraph();
		GraphicNode gn = (GraphicNode) gg.getNode(nodeId);

		Camera cam = viewer.getView("NeoMaPy").getCamera();
		cam.setViewCenter(gn.getX(), gn.getY(), 0);
		cam.setViewPercent(0.1);
	}

	public void resetZoom () {
		View v = viewer.getView("NeoMaPy");
		Camera cam = v.getCamera();
		//cam.setBounds(0, 0, width, height, 0, 0);
		//GraphMetrics gm = cam.getMetrics();
		System.out.println("--- 1 ---\n"+v.getCamera());

		cam.setAutoFitView(true);

//		System.out.println("--- 2 ---\n"+gm);

		this.repaint();
		this.revalidate();

		System.out.println("--- 3 ---\n"+v.getCamera());
	}
	
	public NeoMaPyGraph getGraph() {
		return graph;
	}

	public Viewer getViewer() {
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
		if (graph == null)
			NeoMaPyFrame.error("No Knowledge Graph generated\\Please create it in the \"Conflict Graph\" menu.");
		else {
			graph.processMAP(s);
			rp.setGraphInfo(queries);
		}
	}

	public MAPBar getMAPBar() {
		return rp.getMAPBar();
	}

	public void resetMap(List<Query> queries) {
		if (graph == null)
			NeoMaPyFrame.error("No Knowledge Graph generated\\Please create it in the \"Conflict Graph\" menu.");
		else {
			graph.resetMap();
			rp.setGraphInfo(queries);
		}
	}

	@Override
	public String toString() {
		return "Graph (#nodes:" + graph.getNodeCount() + ",#edges:" + graph.getEdgeCount() + ")";// +graph.edgeAttributes;

	}

	@Override
	public void buttonPushed(String arg0) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void buttonReleased(String arg0) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void mouseLeft(String arg0) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void mouseOver(String arg0) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void viewClosed(String arg0) {
		loop = false;
	}
}
