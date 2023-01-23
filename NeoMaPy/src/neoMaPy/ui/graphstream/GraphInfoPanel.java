package neoMaPy.ui.graphstream;

import java.awt.BorderLayout;
import java.io.IOException;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.atomic.AtomicInteger;

import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTextPane;
import javax.swing.text.BadLocationException;
import javax.swing.text.html.HTMLDocument;
import javax.swing.text.html.HTMLEditorKit;

import org.graphstream.graph.Edge;
import org.graphstream.graph.Node;

import neoMaPy.Query;

public class GraphInfoPanel extends JPanel {
	/**
	 * 
	 */
	private static final long serialVersionUID = 2800380442407155164L;
	private JTextPane graphInfo;
	private NeoMaPyGraph graph;
	private HTMLEditorKit kit = new HTMLEditorKit();
    private HTMLDocument doc = new HTMLDocument();
    public static ReadCSS rc;

	GraphInfoPanel (NeoMaPyGraph graph, int width, int height){
		setLayout(new BorderLayout());
		this.graph = graph;
		rc = new ReadCSS ("conf/NeoMaPy.css");
		add(new JLabel("Graph properties"), BorderLayout.NORTH);
		add(new JScrollPane(graphInfo = new JTextPane()), BorderLayout.CENTER);
		graphInfo.setSize(200, height);
		graphInfo.setContentType("text/html");
		graphInfo.setEditorKit(kit);
		graphInfo.setDocument(doc);
	}

	void setGraphInfo(List<Query> queries) throws BadLocationException, IOException {
		doc = new HTMLDocument ();
		graphInfo.setDocument(doc);

		append("<html>", false, null);
		append("Nodes\n", true, "black");
		setNodeInfo("s");
		setNodeInfo("o");
		setNodeInfo("p");
		setNodeInfo("TF");
		append("<br/>Edges\n", true, "black");
		setConflictInfo(queries);
		append("</html>", false, null);
	}

	double weight = 0.0;int infinity = 0;

	private void setNodeInfo(String type) throws BadLocationException, IOException {
		AtomicInteger nbtotal = new AtomicInteger(0);
		AtomicInteger nbRemoved = new AtomicInteger(0);
		AtomicInteger nbValid = new AtomicInteger(0);
		AtomicInteger nbInvalidRemoved = new AtomicInteger(0);
		AtomicInteger nbValidRemoved = new AtomicInteger(0);
		weight = 0.0d;
		infinity = 0;
		graph.nodes().forEach(n -> {
			String nodeType = (String) n.getAttribute("type");
			if (nodeType != null && nodeType.compareTo(type) == 0) {
				nbtotal.addAndGet(1);
				if(type.compareTo("TF")==0) {
					Boolean removed = (Boolean) n.getAttribute("removed");
					if (removed != null && removed) {
						nbRemoved.addAndGet(1);
					} else {
						double w = (Double)n.getAttribute("weight");
						if(w > NeoMaPyGraph.infinity)	infinity++;
						else							weight += w;
					}
					Boolean valid = (Boolean) n.getAttribute("valid");
					if (valid != null && valid)
						nbValid.addAndGet(1);
					if (removed != null && removed && valid != null && !valid)
						nbInvalidRemoved.addAndGet(1);
					if (removed != null && removed && (valid == null || valid))
						nbValidRemoved.addAndGet(1);
				}
			}
		});
		append(type + ": " + (nbtotal.get()-nbRemoved.get()) + "\n", false, "blue");
		if(type.compareTo("TF")==0) {
			append("Valid: " + Math.round(
					new Float  (nbValid.get()-nbValidRemoved.get())/
					new Float(nbtotal.get()-nbRemoved.get())*10000.0)/100.0 + "%\n", false, "blue");
			append("Removed: " + Math.round(
					new Float(nbRemoved.get())/
					new Float(nbtotal.get())*10000.0)/100.0 + "%\n", false, "blue");
			append("Invalid removed: " + Math.round(
					new Float(nbInvalidRemoved.get())/
					new Float(nbtotal.get()-nbValid.get())*10000)/100 + "%\n", true, "blue");
			append("Graph weight: "+ Math.round(weight*100.0)/100.0 + " (+"+infinity+" inf)", true, "blue");
		}
	}

	private void setConflictInfo(List<Query> queries) throws BadLocationException, IOException {
		Map<String, Integer> edgeAttributes = new HashMap<String, Integer>();
		
		graph.edges().forEach(e -> {
			if(validEdge (e)) {
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
			}
		});

		append("<html>", false, null);
		for(Query q: queries) {
			if(q.instruction.startsWith("Conflict")) {
				String code = q.instruction.substring(q.instruction.indexOf("-")+2);
				String edge =null;
				if(code.indexOf(" -") > -1) {
					code = code.substring(0, code.indexOf(" -"));
					edge = code;
				}
				else {
					if(code.contains("Partial Temporal Consistency")) edge = "pCon";
					else if(code.contains("Partial Temporal Inconsistency")) edge = "pInc";
					else if(code.contains("total Temporal Inconsistency")) edge = "tInc";
					code = "TC1";
				}
				String name = q.instruction.substring(q.instruction.lastIndexOf("-")+2);
				Integer nb = edgeAttributes.get(edge);
				if(nb == null)
					nb = 0;
				append("<b>"+code + "\t("+nb+")</b>\t"+name, false, GraphInfoPanel.rc.getColor(code));
			} else if(q.instruction.contains("Inference")) {
				Integer nb = edgeAttributes.get("inference");
				if(nb == null)
					nb = 0;
				append("<b>Inference\t("+nb+")</b>\t", false, GraphInfoPanel.rc.getColor("inference"));
			}
		}
		append("</html>", false, null);
	}

	private boolean validEdge (Edge e) {
		Node n = e.getSourceNode();
		Boolean removed = (Boolean) n.getAttribute("removed");
		if (removed != null && removed) return false;

		n = e.getTargetNode();
		removed = (Boolean) n.getAttribute("removed");
		if (removed != null && removed) return false;

		return true;
	}
	
	private void append (String text, boolean bold, String c) throws BadLocationException, IOException {
		if(bold)
			text = "<b>"+text+"</b>";
		if(c != null)
			text = "<span style=\"color:"+c+";\">"+text+"</span>";
		kit.insertHTML(doc, doc.getLength(), text, 0, 0, null);
	}
}
