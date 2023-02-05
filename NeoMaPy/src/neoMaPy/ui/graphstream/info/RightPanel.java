/**
 * Created by Nicolas Travers <nicolas.travers@devinci.fr> 2022-2023©
 */
package neoMaPy.ui.graphstream.info;

import java.awt.BorderLayout;
import java.io.IOException;
import java.util.List;

import javax.swing.JPanel;
import javax.swing.text.BadLocationException;

import neoMaPy.Query;
import neoMaPy.ui.graphstream.GraphStreamPanel;

public class RightPanel extends JPanel {
	/**
	 * 
	 */
	private static final long serialVersionUID = -83485516596359808L;
	private SearchPanel searchPanel;
	private NodeInfoPanel nodeInfo;
	private GraphInfoPanel graphInfo;

	public RightPanel(GraphStreamPanel gsp, int width, int height) {
		super();
		setLayout(new BorderLayout());
		setSize(200, height);
		searchPanel = new SearchPanel(gsp, 400, height);
		graphInfo = new GraphInfoPanel(gsp.getGraph(), 400, height);
		nodeInfo = new NodeInfoPanel(gsp.getGraph(), searchPanel, 400, height);
		add(searchPanel, BorderLayout.NORTH);
		add(nodeInfo, BorderLayout.CENTER);
		add(graphInfo, BorderLayout.SOUTH);
	}

	public void setNodeInfo(String nodeId) {
		try {
			nodeInfo.setNodeInfo(nodeId);
		} catch (BadLocationException | IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	public void setGraphInfo(List<Query> queries) {
		try {
			graphInfo.setGraphInfo(queries);
		} catch (BadLocationException | IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
}
