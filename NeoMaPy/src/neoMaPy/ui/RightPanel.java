package neoMaPy.ui;

import java.awt.BorderLayout;
import java.io.IOException;

import javax.swing.JPanel;
import javax.swing.text.BadLocationException;

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
		add(nodeInfo = new NodeInfoPanel(graph, 200, height), BorderLayout.CENTER);
		add(graphInfo = new GraphInfoPanel(graph, 200, height), BorderLayout.SOUTH);
	}

	void setNodeInfo(String nodeId) {
		nodeInfo.setNodeInfo(nodeId);
	}

	void setGraphInfo() {
		try {
			graphInfo.setGraphInfo();
		} catch (BadLocationException | IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
}
