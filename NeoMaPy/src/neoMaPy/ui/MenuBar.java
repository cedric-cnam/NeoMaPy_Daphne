package neoMaPy.ui;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyEvent;

import javax.swing.JMenu;
import javax.swing.JMenuBar;
import javax.swing.JMenuItem;

public class MenuBar extends JMenuBar implements ActionListener {
	private static final long serialVersionUID = -7079284854154034465L;
	GraphStream gs;
	JMenuItem neo4j_load, neo4j_constraint, neo4j_stats,
		graph_css, graph_layout, graph_sop, graph_invalidTF;

	private boolean layoutEnabled = true, displaySop = false, displayInvalidTF = false;
	public MenuBar (GraphStream gs) {
		super ();
		this.gs = gs;

		JMenu m = new JMenu ("Neo4j");
		m.add(neo4j_load = menuItem("Load Graph", 0));
		m.add(neo4j_constraint = menuItem("Constraints", 0));
		m.add(neo4j_stats = menuItem("Graph Stats", 0));
		this.add(m);

		m = new JMenu ("Conflict Graph");
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
		if(o == neo4j_load)
			;
		else if(o == neo4j_constraint)
			;
		else if(o == neo4j_stats)
			;
		else if(o == graph_css)
			gs.getGraph().css();
		else if(o == graph_layout) {
			if (layoutEnabled) {
				gs.viewer.disableAutoLayout();
				graph_layout.setText("Layout: start");
			} else {
				gs.viewer.enableAutoLayout();
				graph_layout.setText("Layout: stop");
			}
			layoutEnabled = !layoutEnabled;
		} else if(o == graph_sop) {
			if (!displaySop) {
				gs.getGraph().setAttribute("ui.stylesheet", "graph {fill-color: gray;}");
				graph_sop.setText("Display sop: true");
			} else {
				gs.getGraph().setAttribute("ui.stylesheet", "graph {fill-color: white;}");
				graph_sop.setText("Display sop: false");
			}
			displaySop = !displaySop;
		} else if(o == graph_invalidTF) {
			if (!displayInvalidTF) {
				gs.getGraph().setAttribute("ui.stylesheet", "node.TF_invalid{stroke-color:red;}");
				graph_invalidTF.setText("Display invalid TF: true");
			} else {
				gs.getGraph().setAttribute("ui.stylesheet", "node.TF_invalid{stroke-color:black;}");
				graph_invalidTF.setText("Display invalid TF: false");
			}
			displayInvalidTF = !displayInvalidTF;
		}

	}
}
