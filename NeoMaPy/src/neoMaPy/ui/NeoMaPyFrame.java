package neoMaPy.ui;

import java.awt.BorderLayout;
import java.awt.Dimension;
import java.awt.Toolkit;

import javax.swing.JFrame;
import javax.swing.JOptionPane;
import javax.swing.JTabbedPane;

import org.graphstream.ui.view.Viewer;

import neoMaPy.MaPy;
import neoMaPy.ui.graphstream.GraphStreamPanel;
import neoMaPy.ui.graphstream.NeoMaPyGraph;
import neoMaPy.ui.neo4j.NeoPanel;

public class NeoMaPyFrame extends JFrame {
	public static JFrame frame;
	GraphStreamPanel gsp;
	NeoPanel neo;
	JTabbedPane tabs;
	/**
	 * 
	 */
	private static final long serialVersionUID = -5767865719882084502L;

	public NeoMaPyFrame () {
		frame = this;
	}
	
	public void init() {
		setLayout(new BorderLayout());
		Dimension screenSize = Toolkit.getDefaultToolkit().getScreenSize();
		int width = new Double(screenSize.getWidth()).intValue();
		int height = new Double(screenSize.getHeight()).intValue();
		setSize(width, height);
		
		add(tabs = new JTabbedPane (), BorderLayout.CENTER);
		
		tabs.addTab("Neo4j", neo = new NeoPanel (width, height));
		neo.connect();
		tabs.addTab("Graph", gsp = new GraphStreamPanel (width, height)); 

		this.setJMenuBar(new MenuBar (this));

		setLocationRelativeTo(null);
		setVisible(true);

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

	public static void error (String message) {
		JOptionPane.showMessageDialog(frame, message);
	}
	
	public void loadGraph () {
		tabs.setSelectedComponent(gsp);
		gsp.initGraph(neo.getQueries());
		this.setAlwaysOnTop(true);
	}
	
	public NeoMaPyGraph getGraph() {
		return gsp.getGraph();
	}

	public Viewer getViewer () {
		return gsp.getViewer();
	}

	public void processMap(MaPy mapy) {
		gsp.processMap(mapy, neo.getQueries());
	}

	public void resetMap(){
		gsp.resetMap(neo.getQueries());
	}
}
