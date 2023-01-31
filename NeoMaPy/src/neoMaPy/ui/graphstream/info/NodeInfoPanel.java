package neoMaPy.ui.graphstream.info;

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

import neoMaPy.ui.graphstream.NeoMaPyGraph;

public class NodeInfoPanel extends JPanel {
	private static final long serialVersionUID = 6707600808327035442L;
	
	private NeoMaPyGraph graph;
	JTextPane nodeText;
	private SearchPanel search;
	//JTextArea edgesText;
	private HTMLEditorKit kit = new HTMLEditorKit();
    private HTMLDocument doc = new HTMLDocument();
    private StringBuffer sb;

	NodeInfoPanel(NeoMaPyGraph graph, SearchPanel search, int width, int height) {
		super ();
		this.graph = graph;
		setLayout(new BorderLayout ());
		this.search = search;
		
		JPanel p = new JPanel (new BorderLayout ());
		p.add(new JLabel("Node Information            "), BorderLayout.NORTH);
		p.add(new JScrollPane (nodeText = new JTextPane()), BorderLayout.CENTER);
		nodeText.setSize(width, height);
		nodeText.setContentType("text/html");
		nodeText.setEditorKit(kit);
		nodeText.setDocument(doc);

		add(p, BorderLayout.CENTER);
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
		search.setNodeId(ID);
		sb = new StringBuffer ("<html><table><tr><th colspan=3 style=\"border:1px;\"><b>Nodes</b></th></tr>");
		//append("<span style=\"font-size:8px;\">NodeId: "+ID+"</span>", false, "gray");
		
		append("Type", type, "", false, null);
		if (name != null)append("Name", name, "", false, null);
		if (weight != null)append("Weight", weight, "", false, null);
		if (polarity != null)append("Polarity", polarity, "", false, null);
		if (date_start != null)append("Date_start", date_start, "", false, null);
		if (date_end != null)append("Date_end", date_end, "", false, null);
		if (valid != null)append("Valid", valid, "", false, null);

		if(type.compareTo("TF")==0) {
			n.edges().forEach(e -> {
				e.attributeKeys().forEach(att -> {
					if(att.compareTo("o") ==0 || att.compareTo("s") == 0 || att.compareTo("p") == 0)
						try {
							append(att, e.getTargetNode().getAttribute("name").toString(), e.getTargetNode().getId(), false, "gray");
						} catch (BadLocationException | IOException e1) {
							// TODO Auto-generated catch block
							e1.printStackTrace();
						}
				});
			});
		}
		sb.append("<tr><th colspan=3 style=\"border:1px;\"><b>Edges</b></th></tr>");

		conflicts (n);
		sb.append("</table></html>");
		kit.insertHTML(doc, doc.getLength(), sb.toString(), 0, 0, null);

	}

	private void conflicts (Node n) throws BadLocationException, IOException {
		Map<String, Integer> edgeAttributes = new HashMap<String, Integer>();
		n.edges().forEach(e -> {
			e.attributeKeys().forEach(att -> {
				if(att.compareTo("o") ==0 || att.compareTo("s") == 0 || att.compareTo("p") == 0 || att.compareTo("ui.class") == 0 || att.compareTo("ui.hide") == 0)
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
				String color = GraphInfoPanel.rc.getColor(e); 
				append(e, i+"", "", false, color);
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

	private void append (String key, String value, String info, boolean bold, String c) throws BadLocationException, IOException {
		sb.append("<tr style=\"color:"+c+";\"><td>"+(bold?"<b>":"")+key+(bold?"</b>":"")+ "</b></td><td><b>"+value+"</b></td><td>"+info+"</td></tr>");
	}
}
