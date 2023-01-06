package neoMaPy.ui;

import java.awt.BorderLayout;
import java.util.HashMap;
import java.util.Map;

import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTextArea;

import org.graphstream.graph.Node;

public class NodeInfoPanel extends JPanel {
	private static final long serialVersionUID = 6707600808327035442L;
	
	private NeoMaPyGraph graph;
	JTextArea nodeText;
	JTextArea edgesText;

	NodeInfoPanel(NeoMaPyGraph graph, int width, int height) {
		super ();
		this.graph = graph;
		setLayout(new BorderLayout ());
		
		JPanel p = new JPanel (new BorderLayout ());
		p.add(new JLabel("Node Information"), BorderLayout.NORTH);
		p.add(new JScrollPane (nodeText = new JTextArea (20, 20)), BorderLayout.CENTER);
		nodeText.setText("\n\n\n\n\n\n\n\n\n\n\n\n");
		nodeText.setSize(width, height);
		nodeText.setLineWrap(true);
		add(p, BorderLayout.CENTER);

		p = new JPanel (new BorderLayout ());
		p.add(new JLabel("Node's edges Information"), BorderLayout.NORTH);
		p.add(new JScrollPane (edgesText = new JTextArea (20, 10)), BorderLayout.CENTER);
		edgesText.setText("\n\n\n");
		edgesText.setSize(width, height);
		edgesText.setLineWrap(true);
		add(p, BorderLayout.SOUTH);
	}

	void setNodeInfo(String nodeId) {
		Node n = graph.getNode(nodeId);
		if(n == null) {
			nodeText.setText("");
			edgesText.setText("");
			return;
		}

		String name = getAttribute(n, "name");
		String type = getAttribute(n, "type");
		String weight = getAttribute(n, "weight");
		String polarity = getAttribute(n, "polarity");
		String date_start = getAttribute(n, "date_start");
		if (date_start != null && date_start.length() > 0)
			date_start = date_start.substring(0, date_start.indexOf("T"));
		String date_end = getAttribute(n, "date_end");
		if (date_end != null && date_end.length() > 0)
			date_end = date_end.substring(0, date_end.indexOf("T"));
		String valid = getAttribute(n, "valid");
		String ID = n.getId();

		StringBuffer sb = new StringBuffer ("Node Type: "+type);
		if (name != null)sb.append("\nName: " + name);
		if (weight != null)sb.append("\nWeight: " + weight);
		if (polarity != null)sb.append("\nPolarity: " + polarity);
		if (date_start != null)sb.append("\nDate_start: " + date_start);
		if (date_end != null)sb.append("\nDate_end: " + date_end);
		if (valid != null)sb.append("\nValid: " + valid);
		sb.append("\nNodeId: "+ID);
				
		nodeText.setText(sb.toString());
		conflicts (n);
	}

	private void conflicts (Node n) {
		StringBuffer sb = new StringBuffer ("");
		Map<String, Integer> edgeAttributes = new HashMap<String, Integer>();
		n.edges().forEach(e -> {
			e.attributeKeys().forEach(att -> {
				if(att.compareTo("o") ==0 || att.compareTo("s") == 0 || att.compareTo("p") == 0 || att.compareTo("ui.class") == 0)
					return;
				Integer val = edgeAttributes.get(att);
				if (val == null)
					val = 1;
				else
					val++;
				edgeAttributes.put(att, val);
			});
		});
		edgeAttributes.keySet().forEach(e -> {
			Integer i = edgeAttributes.get(e);
			sb.append(e+": "+i+"\n");
		});
		edgesText.setText(sb.toString());
	}

	private String getAttribute(Node n, String att) {
		Object o = n.getAttribute(att);
		if (o == null)
			return null;
		return o.toString();
	}
}
