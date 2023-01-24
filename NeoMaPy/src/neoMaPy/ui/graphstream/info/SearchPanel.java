package neoMaPy.ui.graphstream.info;

import java.awt.BorderLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.JButton;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JTextField;

import neoMaPy.ui.graphstream.GraphStreamPanel;

public class SearchPanel extends JPanel implements ActionListener {
	private static final long serialVersionUID = 6707600808327035442L;
	
	private GraphStreamPanel gsp;
	JTextField nodeText;
	JButton search;

	SearchPanel(GraphStreamPanel gsp, int width, int height) {
		super ();
		this.gsp = gsp;
		setLayout(new BorderLayout ());
		
		add(new JLabel ("NodeId search"), BorderLayout.NORTH);
		add(nodeText = new JTextField(), BorderLayout.CENTER);
		add(search = new JButton("Search"), BorderLayout.EAST);
		search.addActionListener(this);
	}

	@Override
	public void actionPerformed(ActionEvent e) {
		String nodeId = nodeText.getText();
		gsp.zoomOnNode(nodeId);
	}
}
