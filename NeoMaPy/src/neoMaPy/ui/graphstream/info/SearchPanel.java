/**
 * Created by Nicolas Travers <nicolas.travers@devinci.fr> 2022-2023©
 */
package neoMaPy.ui.graphstream.info;

import java.awt.BorderLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.JButton;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JTextArea;
import javax.swing.JTextField;

import neoMaPy.ui.graphstream.GraphStreamPanel;

public class SearchPanel extends JPanel implements ActionListener {
	private static final long serialVersionUID = 6707600808327035442L;
	
	private GraphStreamPanel gsp;
	private JTextArea nodeText;
	private JButton search;

	SearchPanel(GraphStreamPanel gsp, int width, int height) {
		super ();
		this.gsp = gsp;
		setLayout(new BorderLayout ());
		
		add(new JLabel ("NodeId Zoom"), BorderLayout.NORTH);
		add(nodeText = new JTextArea(2,10), BorderLayout.CENTER);
		nodeText.setLineWrap(true);
		add(search = new JButton("Search"), BorderLayout.EAST);
		search.addActionListener(this);
	}

	@Override
	public void actionPerformed(ActionEvent e) {
		String nodeId = nodeText.getText();
		gsp.zoomOnNode(nodeId);
	}

	public void setNodeId (String nodeId) {
		nodeText.setText(nodeId);
	}
}
