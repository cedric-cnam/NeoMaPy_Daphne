package neoMaPy.ui;

import java.awt.BorderLayout;
import java.awt.Dimension;
import java.awt.Toolkit;

import javax.swing.JFrame;
import javax.swing.JTabbedPane;

import org.graphstream.ui.view.Viewer;

import neoMaPy.ui.graphstream.GraphStreamPanel;
import neoMaPy.ui.graphstream.NeoMaPyGraph;
import neoMaPy.ui.neo4j.NeoPanel;

public class NeoMaPyFrame extends JFrame {

	GraphStreamPanel gsp;
	NeoPanel neo;
	JTabbedPane tabs;
	/**
	 * 
	 */
	private static final long serialVersionUID = -5767865719882084502L;

	public NeoMaPyFrame () {
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

	public void loadGraph () {
		gsp.initGraph();
	}
	
	public NeoMaPyGraph getGraph() {
		return gsp.getGraph();
	}

	public Viewer getViewer () {
		return gsp.getViewer();
	}
}
