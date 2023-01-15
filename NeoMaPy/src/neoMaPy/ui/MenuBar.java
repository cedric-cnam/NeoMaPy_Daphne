package neoMaPy.ui;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyEvent;

import javax.swing.JMenu;
import javax.swing.JMenuBar;
import javax.swing.JMenuItem;

public class MenuBar extends JMenuBar implements ActionListener {
	private static final long serialVersionUID = -7079284854154034465L;
	NeoMaPyFrame neomapy;
	JMenuItem graph_load, neo4j_connect, neo4j_queries,
		graph_css, graph_layout, graph_sop, graph_invalidTF;

	private boolean layoutEnabled = true, displaySop = false, displayInvalidTF = false;
	public MenuBar (NeoMaPyFrame neomapy) {
		super ();
		this.neomapy = neomapy;

		JMenu m = new JMenu ("Neo4j");
		m.add(neo4j_connect = menuItem("Connect to Neo4j", 0));
		m.add(neo4j_queries = menuItem("Execute all queries", 0));
		this.add(m);

		m = new JMenu ("Conflict Graph");
		m.add(graph_load = menuItem("Load Knowledge Graph", 0));
		m.add(graph_css = menuItem("Reload CSS", KeyEvent.VK_C));
		m.add(graph_layout = menuItem("Layout: stop", KeyEvent.VK_L));
		m.add(graph_sop = menuItem("Display sop: false", 0));
		m.add(graph_invalidTF = menuItem("Display invalid TF: false", 0));
		this.add(m);

	}

	private JMenuItem menuItem (String name, int key) {
		JMenuItem mi = new JMenuItem (name);
		if (key > 0)
			mi.setMnemonic(key);
		mi.addActionListener(this);
		return mi;
	}
	
	@Override
	public void actionPerformed(ActionEvent e) {
		Object o = e.getSource();
		if(o == graph_load)
			neomapy.loadGraph();
		else if(o == neo4j_connect)
			neomapy.neo.connect();
		else if(o == neo4j_queries)
			neomapy.neo.executeQueries();
		else if(o == graph_css)
			neomapy.getGraph().css();
		else if(o == graph_layout) {
			if (layoutEnabled) {
				neomapy.getViewer().disableAutoLayout();
				graph_layout.setText("Layout: start");
			} else {
				neomapy.getViewer().enableAutoLayout();
				graph_layout.setText("Layout: stop");
			}
			layoutEnabled = !layoutEnabled;
		} else if(o == graph_sop) {
			if (!displaySop) {
				neomapy.getGraph().setAttribute("ui.stylesheet", "graph {fill-color: gray;}");
				graph_sop.setText("Display sop: true");
			} else {
				neomapy.getGraph().setAttribute("ui.stylesheet", "graph {fill-color: white;}");
				graph_sop.setText("Display sop: false");
			}
			displaySop = !displaySop;
		} else if(o == graph_invalidTF) {
			if (!displayInvalidTF) {
				neomapy.getGraph().setAttribute("ui.stylesheet", "node.TF_invalid{stroke-color:red;}");
				graph_invalidTF.setText("Display invalid TF: true");
			} else {
				neomapy.getGraph().setAttribute("ui.stylesheet", "node.TF_invalid{stroke-color:black;}");
				graph_invalidTF.setText("Display invalid TF: false");
			}
			displayInvalidTF = !displayInvalidTF;
		}

	}
}
