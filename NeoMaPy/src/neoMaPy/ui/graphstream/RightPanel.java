package neoMaPy.ui.graphstream;

import java.awt.BorderLayout;
import java.io.IOException;
import java.util.List;

import javax.swing.JPanel;
import javax.swing.text.BadLocationException;

import neoMaPy.Query;

public class RightPanel extends JPanel {
	/**
	 * 
	 */
	private static final long serialVersionUID = -83485516596359808L;
	private NodeInfoPanel nodeInfo;
	private GraphInfoPanel graphInfo;

	RightPanel(NeoMaPyGraph graph, int width, int height) {
		super();
		setLayout(new BorderLayout());
		setSize(200, height);
		graphInfo = new GraphInfoPanel(graph, 400, height);
		nodeInfo = new NodeInfoPanel(graph, 400, height);
		add(nodeInfo, BorderLayout.CENTER);
		add(graphInfo, BorderLayout.SOUTH);
	}

	void setNodeInfo(String nodeId) {
		try {
			nodeInfo.setNodeInfo(nodeId);
		} catch (BadLocationException | IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	void setGraphInfo(List<Query> queries) {
		try {
			graphInfo.setGraphInfo(queries);
		} catch (BadLocationException | IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
}
