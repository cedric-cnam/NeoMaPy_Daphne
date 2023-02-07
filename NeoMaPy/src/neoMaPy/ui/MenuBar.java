/**
 * Created by Nicolas Travers <nicolas.travers@devinci.fr> 2022-2023©
 */
package neoMaPy.ui;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.ItemEvent;
import java.awt.event.ItemListener;
import java.awt.event.KeyEvent;

import javax.swing.ButtonGroup;
import javax.swing.JLabel;
import javax.swing.JMenu;
import javax.swing.JMenuBar;
import javax.swing.JMenuItem;
import javax.swing.JRadioButtonMenuItem;
import javax.swing.JSeparator;
import javax.swing.JSlider;
import javax.swing.KeyStroke;
import javax.swing.event.ChangeEvent;
import javax.swing.event.ChangeListener;

import neoMaPy.MaPy;
import neoMaPy.MaPyStrategy.MaPyStrategy;

public class MenuBar extends JMenuBar implements ActionListener, ItemListener, ChangeListener {
	private static final long serialVersionUID = -7079284854154034465L;
	NeoMaPyFrame neomapy;
	JMenuItem graph_load, neo4j_connect, neo4j_queries, graph_css, graph_layout, graph_sop, graph_invalidTF, processMAP,
			resetMAP, randomMAP, conflictDecreasingMAP, conflictIncreasingMAP, weightDecreasingMAP, weightIncreasingMAP,
			invalidMAP;
	JRadioButtonMenuItem[] tempC = new JRadioButtonMenuItem[4];
	int tempCons = 0;
	double threshold = 0.0;
	JMenu topK, cons, thresholdMenu;
	int topKv = MaPyStrategy.minTopK;
	int scaleTopK = 50;
	JSlider sliderTopK, sliderThreshold;

	private boolean layoutEnabled = true, displaySop = false, displayInvalidTF = false;

	public MenuBar(NeoMaPyFrame neomapy) {
		super();
		this.neomapy = neomapy;

		JMenu m = new JMenu("Neo4j");
		m.add(neo4j_connect = menuItem("Connect to Neo4j", 0));
		m.add(neo4j_queries = menuItem("Execute all queries", 0));
		this.add(m);

		m = new JMenu("Conflict Graph");
		m.add(graph_load = menuItem("Load Knowledge Graph", KeyEvent.VK_G));
		m.add(graph_css = menuItem("Reload CSS", KeyEvent.VK_C));
		m.add(graph_layout = menuItem("Layout: stop", KeyEvent.VK_L));
		m.add(graph_sop = menuItem("Display sop: false", KeyEvent.VK_S));
		m.add(graph_invalidTF = menuItem("Display invalid TF: false", KeyEvent.VK_I));
		this.add(m);

		m = new JMenu("MAP Inference");
		m.add(new JLabel("NeoMaPy"));
		cons = new JMenu("Temporal Consistency - tCon");
		ButtonGroup bg = new ButtonGroup();
		cons.add(radioMenuItem("tCon - Total Consistency", MaPyStrategy.tCon, true, bg));
		cons.add(radioMenuItem("pCon - Partial Consistency", MaPyStrategy.pCon, false, bg));
		cons.add(radioMenuItem("pInc - Partial Inconsistency", MaPyStrategy.pInc, false, bg));
		cons.add(radioMenuItem("tInc - Total Inconsistency", MaPyStrategy.tInc, false, bg));
		m.add(cons);

		topK = new JMenu("Top-" + (MaPyStrategy.minTopK));
		sliderTopK = new JSlider(MaPyStrategy.minTopK / scaleTopK, MaPyStrategy.maxTopK / scaleTopK);
		sliderTopK.setValue(MaPyStrategy.minTopK / scaleTopK);
		sliderTopK.addChangeListener(this);
		topK.add(sliderTopK);
		m.add(topK);

		thresholdMenu = new JMenu("Threshold-" + new Double(MaPyStrategy.minThreshold).doubleValue() / 10.0);
		sliderThreshold = new JSlider(MaPyStrategy.minThreshold, MaPyStrategy.maxThreshold);
		sliderThreshold.setValue(MaPyStrategy.minThreshold);
		sliderThreshold.addChangeListener(this);
		thresholdMenu.add(sliderThreshold);
		m.add(thresholdMenu);

		m.add(processMAP = menuItem("Compute MAP Inference", KeyEvent.VK_M));
		m.add(new JSeparator());

		m.add(resetMAP = menuItem("reset", KeyEvent.VK_R));

		JMenu test = new JMenu("MAP test");
		test.add(randomMAP = menuItem("Random nodes", 0));
		test.add(conflictDecreasingMAP = menuItem("Decreasing Nb conflict order", 0));
		test.add(conflictIncreasingMAP = menuItem("Increasing Nb conflict order", 0));
		test.add(weightDecreasingMAP = menuItem("Decreasing Weight order", 0));
		test.add(weightIncreasingMAP = menuItem("Increasing Weight order", 0));
		test.add(invalidMAP = menuItem("Only invalid nodes (goal)", 0));
		m.add(test);

		this.add(m);
	}

	private JMenuItem menuItem(String name, int key) {
		JMenuItem mi = new JMenuItem(name);
		if (key > 0) {
			mi.setMnemonic(key);
			mi.addActionListener(this);
			mi.setAccelerator(KeyStroke.getKeyStroke(key, ActionEvent.CTRL_MASK));
		}
		mi.addActionListener(this);
		return mi;
	}

	private JRadioButtonMenuItem radioMenuItem(String name, int i, boolean selected, ButtonGroup bg) {
		JRadioButtonMenuItem mi = new JRadioButtonMenuItem(name, selected);
		mi.addItemListener(this);
		tempC[i] = mi;
		bg.add(mi);
		return mi;
	}

	long when = 0;

	@Override
	public void actionPerformed(ActionEvent e) {
		if (when == e.getWhen())
			return;
		when = e.getWhen();
		Object o = e.getSource();
		if (o == graph_load)
			neomapy.loadGraph();
		else if (o == neo4j_connect)
			neomapy.neo.connect();
		else if (o == neo4j_queries)
			neomapy.neo.executeQueries();
		else if (o == graph_css)
			neomapy.getGraph().css();
		else if (o == graph_layout) {
			if (layoutEnabled) {
				neomapy.getViewer().disableAutoLayout();
				graph_layout.setText("Layout: start");
			} else {
				neomapy.getViewer().enableAutoLayout();
				graph_layout.setText("Layout: stop");
			}
			layoutEnabled = !layoutEnabled;
		} else if (o == graph_sop) {
			if (!displaySop) {
				neomapy.getGraph().setAttribute("ui.stylesheet", "graph {fill-color: gray;}");
				graph_sop.setText("Display sop: true");
			} else {
				neomapy.getGraph().setAttribute("ui.stylesheet", "graph {fill-color: white;}");
				graph_sop.setText("Display sop: false");
			}
			displaySop = !displaySop;
		} else if (o == graph_invalidTF) {
			if (!displayInvalidTF) {
				neomapy.getGraph().setAttribute("ui.stylesheet", "node.TF_invalid{stroke-color:red;}");
				graph_invalidTF.setText("Display invalid TF: true");
			} else {
				neomapy.getGraph().setAttribute("ui.stylesheet", "node.TF_invalid{stroke-color:black;}");
				graph_invalidTF.setText("Display invalid TF: false");
			}
			displayInvalidTF = !displayInvalidTF;
		} else if (o == resetMAP)
			neomapy.resetMap();
		else if (o == processMAP) {
			setMAPLabel(MaPyStrategy.tcons(tempCons) + ", top-" + topKv + ", w > " + threshold);
			neomapy.processMAP(
					MaPy.strategy(tempCons, topKv, threshold, neomapy.getGraph().getMapping(), neomapy.getMAPBar()));
		} else if (o == randomMAP) {
			setMAPLabel("Random");
			neomapy.processMAP(MaPy.strategy(MaPy.RANDOM_STRATEGY, neomapy.getMAPBar()));
		} else if (o == conflictIncreasingMAP) {
			setMAPLabel("Increasing conflicts");
			neomapy.processMAP(MaPy.strategy(MaPy.CONFLICT_INCREASING_STRATEGY, neomapy.getMAPBar()));
		} else if (o == conflictDecreasingMAP) {
			setMAPLabel("Decreasing conflicts");
			neomapy.processMAP(MaPy.strategy(MaPy.CONFLICT_DECREASING_STRATEGY, neomapy.getMAPBar()));
		} else if (o == weightIncreasingMAP) {
			setMAPLabel("Increasing weight");
			neomapy.processMAP(MaPy.strategy(MaPy.WEIGHT_INCREASING_STRATEGY, neomapy.getMAPBar()));
		} else if (o == weightDecreasingMAP) {
			setMAPLabel("Decreasing weight");
			neomapy.processMAP(MaPy.strategy(MaPy.WEIGHT_DECREASING_STRATEGY, neomapy.getMAPBar()));
		} else if (o == invalidMAP) {
			setMAPLabel("Only invalid");
			neomapy.processMAP(MaPy.strategy(MaPy.GOAL_STRATEGY, neomapy.getMAPBar()));
		}
	}

	@Override
	public void itemStateChanged(ItemEvent e) {
		Object o = e.getSource();
		if (o == tempC[0] && tempC[0].isSelected()) {
			tempCons = MaPyStrategy.tCon;
			cons.setText("Temporal Consistency - tCon");
		} else if (o == tempC[1] && tempC[1].isSelected()) {
			tempCons = MaPyStrategy.pCon;
			cons.setText("Temporal Consistency - pCon");
		} else if (o == tempC[2] && tempC[2].isSelected()) {
			tempCons = MaPyStrategy.pInc;
			cons.setText("Temporal Consistency - pInc");
		} else if (o == tempC[3] && tempC[3].isSelected()) {
			tempCons = MaPyStrategy.tInc;
			cons.setText("Temporal Consistency - tInc");
		}
	}

	@Override
	public void stateChanged(ChangeEvent e) {
		if (e.getSource() == sliderTopK) {
			topKv = sliderTopK.getValue() * scaleTopK;
			topK.setText("Top-" + topKv);
		} else if (e.getSource() == sliderThreshold) {
			threshold = new Double(sliderThreshold.getValue()).doubleValue() / 10.0;
			thresholdMenu.setText("Threshold-" + threshold);
		}
	}

	public void setMAPLabel(String label) {
		neomapy.getMAPBar().setLabel(label);
	}
}
