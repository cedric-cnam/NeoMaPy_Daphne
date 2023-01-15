package neoMaPy.ui.graphstream;

import java.awt.BorderLayout;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTextPane;
import javax.swing.text.BadLocationException;
import javax.swing.text.html.HTMLDocument;
import javax.swing.text.html.HTMLEditorKit;

import org.graphstream.graph.Node;

public class NodeInfoPanel extends JPanel {
	private static final long serialVersionUID = 6707600808327035442L;
	
	private NeoMaPyGraph graph;
	JTextPane nodeText;
	//JTextArea edgesText;
	private HTMLEditorKit kit = new HTMLEditorKit();
    private HTMLDocument doc = new HTMLDocument();

	NodeInfoPanel(NeoMaPyGraph graph, int width, int height) {
		super ();
		this.graph = graph;
		setLayout(new BorderLayout ());
		
		JPanel p = new JPanel (new BorderLayout ());
		p.add(new JLabel("Node Information            "), BorderLayout.NORTH);
		p.add(new JScrollPane (nodeText = new JTextPane()), BorderLayout.CENTER);
		nodeText.setSize(width, height);
		nodeText.setContentType("text/html");
		nodeText.setEditorKit(kit);
		nodeText.setDocument(doc);


		//nodeText.setText("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n");
		//nodeText.setSize(width, height);
		//nodeText.setLineWrap(true);
		add(p, BorderLayout.CENTER);
/*
		p = new JPanel (new BorderLayout ());
		p.add(new JLabel("Node's edges Information"), BorderLayout.NORTH);
		p.add(new JScrollPane (edgesText = new JTextArea (20, 10)), BorderLayout.CENTER);
		edgesText.setText("\n\n\n");
		//edgesText.setSize(width, height);
		edgesText.setLineWrap(true);
		add(p, BorderLayout.SOUTH);*/
	}

	void setNodeInfo(String nodeId) throws BadLocationException, IOException {
		Node n = graph.getNode(nodeId);
		if(n == null) {
			nodeText.setText("");
			//edgesText.setText("");
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
		
		doc = new HTMLDocument ();
		nodeText.setDocument(doc);
		append("<html>", false, null);
		append("<span style=\"font-size:8px;\">NodeId: "+ID+"</span>", false, "gray");
		
		append("Node Type: "+type, true, null);
		if (name != null)append("\nName: " + name, false, null);
		if (weight != null)append("\nWeight: " + weight, false, null);
		if (polarity != null)append("\nPolarity: " + polarity, false, null);
		if (date_start != null)append("\nDate_start: " + date_start, false, null);
		if (date_end != null)append("\nDate_end: " + date_end, false, null);
		if (valid != null)append("\nValid: " + valid, false, null);
		
		if(type.compareTo("TF")==0) {
			n.edges().forEach(e -> {
				e.attributeKeys().forEach(att -> {
					if(att.compareTo("o") ==0 || att.compareTo("s") == 0 || att.compareTo("p") == 0)
						try {
							append("\n"+att+": "+e.getTargetNode().getId(), false, "gray");
						} catch (BadLocationException | IOException e1) {
							// TODO Auto-generated catch block
							e1.printStackTrace();
						}
				});
			});
		}
		
		conflicts (n);
		append("</html>", false, null);
	}

	private void conflicts (Node n) throws BadLocationException, IOException {
		append("<br/>Edges", true, null);
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
			try {
				append(e+": "+i+"\n", false, null);
			} catch (BadLocationException | IOException e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			}
		});
		//edgesText.setText(sb.toString());
	}

	private String getAttribute(Node n, String att) {
		Object o = n.getAttribute(att);
		if (o == null)
			return null;
		return o.toString();
	}

	private void append (String text, boolean bold, String c) throws BadLocationException, IOException {
		if(bold)
			text = "<b>"+text+"</b>";
		if(c != null)
			text = "<span style=\"color:"+c+";\">"+text+"</span>";
		kit.insertHTML(doc, doc.getLength(), text, 0, 0, null);
	}
}
