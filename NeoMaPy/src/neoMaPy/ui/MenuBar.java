package neoMaPy.ui;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.ItemEvent;
import java.awt.event.ItemListener;
import java.awt.event.KeyEvent;

import javax.swing.ButtonGroup;
import javax.swing.JMenu;
import javax.swing.JMenuBar;
import javax.swing.JMenuItem;
import javax.swing.JRadioButtonMenuItem;
import javax.swing.JSlider;
import javax.swing.KeyStroke;
import javax.swing.event.ChangeEvent;
import javax.swing.event.ChangeListener;

import neoMaPy.MaPy;

public class MenuBar extends JMenuBar implements ActionListener, ItemListener, ChangeListener {
	private static final long serialVersionUID = -7079284854154034465L;
	NeoMaPyFrame neomapy;
	JMenuItem graph_load, neo4j_connect, neo4j_queries,
		graph_css, graph_layout, graph_sop, graph_invalidTF,
		processMAP, resetMAP,
		randomMAP, conflictDecreasingMAP, conflictIncreasingMAP, weightDecreasingMAP, weightIncreasingMAP, invalidMAP;
	JRadioButtonMenuItem [] tempC = new JRadioButtonMenuItem [4];int tempCons=0;
	JMenu topK, cons;int topKv = 10;JSlider slider;

	private boolean layoutEnabled = true, displaySop = false, displayInvalidTF = false;
	public MenuBar (NeoMaPyFrame neomapy) {
		super ();
		this.neomapy = neomapy;

		JMenu m = new JMenu ("Neo4j");
		m.add(neo4j_connect = menuItem("Connect to Neo4j", 0));
		m.add(neo4j_queries = menuItem("Execute all queries", 0));
		this.add(m);

		m = new JMenu ("Conflict Graph");
		m.add(graph_load = menuItem("Load Knowledge Graph", KeyEvent.VK_G));
		m.add(graph_css = menuItem("Reload CSS", KeyEvent.VK_C));
		m.add(graph_layout = menuItem("Layout: stop", KeyEvent.VK_L));
		m.add(graph_sop = menuItem("Display sop: false", KeyEvent.VK_S));
		m.add(graph_invalidTF = menuItem("Display invalid TF: false", KeyEvent.VK_I));
		this.add(m);

		m = new JMenu ("MAP Inference");
		cons = new JMenu ("Temporal Consistency - tCon");
		ButtonGroup bg = new ButtonGroup ();
		cons.add (radioMenuItem("tCon - Total Consistency", 0, true, bg));
		cons.add (radioMenuItem("pCon - Partial Consistency", 1, false, bg));
		cons.add (radioMenuItem("pInc - Partial Inconsistency", 2, false, bg));
		cons.add (radioMenuItem("tInc - Total Inconsistency", 3, false, bg));
		m.add(cons);
		
		topK = new JMenu ("Top-10");
		slider = new JSlider(3, 20);
		slider.setValue(10);
        slider.addChangeListener(this);
        topK.add(slider);
        m.add(topK);  
        
        m.add(processMAP = menuItem("process", KeyEvent.VK_M));
        m.add(resetMAP = menuItem("reset", KeyEvent.VK_R));
        
        JMenu test = new JMenu ("MAP test");
        test.add(randomMAP = menuItem("Random nodes", 0));
        test.add(conflictDecreasingMAP = menuItem("Decreasing Nb conflict order", 0));
        test.add(conflictIncreasingMAP = menuItem("Increasing Nb conflict order", 0));
        test.add(weightDecreasingMAP = menuItem("Decreasing Weight order", 0));
        test.add(weightIncreasingMAP = menuItem("Increasing Weight order", 0));
        test.add(invalidMAP = menuItem("Only invalid nodes (goal)", 0));
        m.add(test);
		
		this.add(m);
	}

	private JMenuItem menuItem (String name, int key) {
		JMenuItem mi = new JMenuItem (name);
		if (key > 0) {
			mi.setMnemonic(key);
			mi.addActionListener(this);
			mi.setAccelerator(KeyStroke.getKeyStroke(key,ActionEvent.CTRL_MASK));
		}
		mi.addActionListener(this);
		return mi;
	}

	private JRadioButtonMenuItem radioMenuItem (String name, int i, boolean selected, ButtonGroup bg) {
		JRadioButtonMenuItem mi = new JRadioButtonMenuItem (name, selected);
		mi.addItemListener(this);
		tempC[i] = mi;
		bg.add(mi);
		return mi;
	}

	long time = System.currentTimeMillis();
	
	@Override
	public void actionPerformed(ActionEvent e) {
		if(System.currentTimeMillis() - time < 500)return;time = System.currentTimeMillis();
		Object o = e.getSource();
		if(o == graph_load)			neomapy.loadGraph();
		else if(o == neo4j_connect)	neomapy.neo.connect();
		else if(o == neo4j_queries)	neomapy.neo.executeQueries();
		else if(o == graph_css)		neomapy.getGraph().css();
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
		} else if (o == resetMAP)			neomapy.resetMap();
		else if (o == processMAP)			neomapy.processMap (new MaPy (tempCons, topKv));
		else if(o == randomMAP)				neomapy.processMap (new MaPy (MaPy.RANDOM_STRATEGY));
		else if(o == conflictIncreasingMAP)	neomapy.processMap (new MaPy (MaPy.CONFLICT_INCREASING_STRATEGY));
		else if(o == conflictDecreasingMAP)	neomapy.processMap (new MaPy (MaPy.CONFLICT_DECREASING_STRATEGY));
		else if(o == weightIncreasingMAP)	neomapy.processMap (new MaPy (MaPy.WEIGHT_INCREASING_STRATEGY));
		else if(o == weightDecreasingMAP)	neomapy.processMap (new MaPy (MaPy.WEIGHT_DECREASING_STRATEGY));
		else if(o == invalidMAP)			neomapy.processMap (new MaPy (MaPy.GOAL_STRATEGY));
	}

	@Override
	public void itemStateChanged(ItemEvent e) {
		Object o = e.getSource();
		if(o == tempC[0] && tempC[0].isSelected()) {tempCons=0;cons.setText("Temporal Consistency - tCon");}
		else if(o == tempC[1] && tempC[1].isSelected()){tempCons=1;cons.setText("Temporal Consistency - pCon");}
		else if(o == tempC[2] && tempC[2].isSelected()){tempCons=2;cons.setText("Temporal Consistency - pInc");}
		else if(o == tempC[3] && tempC[3].isSelected()){tempCons=3;cons.setText("Temporal Consistency - tInc");}
	}

	@Override
	public void stateChanged(ChangeEvent e) {
		if(e.getSource() == slider) {
			topKv = slider.getValue();
			topK.setText("Top-"+topKv);
		}
	}
}
