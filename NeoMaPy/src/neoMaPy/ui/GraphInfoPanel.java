package neoMaPy.ui;

import java.awt.BorderLayout;
import java.awt.Color;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.atomic.AtomicInteger;

import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTextPane;
import javax.swing.text.AttributeSet;
import javax.swing.text.BadLocationException;
import javax.swing.text.SimpleAttributeSet;
import javax.swing.text.StyleConstants;
import javax.swing.text.StyleContext;
import javax.swing.text.html.HTMLDocument;
import javax.swing.text.html.HTMLEditorKit;

public class GraphInfoPanel extends JPanel {
	/**
	 * 
	 */
	private static final long serialVersionUID = 2800380442407155164L;
	private JTextPane graphInfo;
	private NeoMaPyGraph graph;
	private HTMLEditorKit kit = new HTMLEditorKit();
    private HTMLDocument doc = new HTMLDocument();
   
	GraphInfoPanel (NeoMaPyGraph graph, int width, int height){
		setLayout(new BorderLayout());
		this.graph = graph;
		add(new JLabel("Graph properties"), BorderLayout.NORTH);
		add(new JScrollPane(graphInfo = new JTextPane()), BorderLayout.CENTER);
		graphInfo.setSize(200, height);
		graphInfo.setContentType("text/html");
		graphInfo.setEditorKit(kit);
		graphInfo.setDocument(doc);
	}

	void setGraphInfo() throws BadLocationException, IOException {
		append("<html>", false, null);
		append("Nodes\n", true, Color.black);
		setNodeInfo("s");
		setNodeInfo("o");
		setNodeInfo("p");
		setNodeInfo("TF");
		append("<br/>Edges\n", true, Color.black);
		setEdgesInfo();
		append("</html>", false, null);
	}

	private void setNodeInfo(String type) throws BadLocationException, IOException {
		AtomicInteger nb = new AtomicInteger(0);
		graph.nodes().forEach(n -> {
			String nodeType = (String) n.getAttribute("type");
			if (nodeType != null && nodeType.compareTo(type) == 0) {
				nb.addAndGet(1);
			}
		});
		append(type + ": " + nb.get() + "\n", false, Color.blue);
	}

	private void setEdgesInfo() {
		Map<String, Integer> edgeAttributes = new HashMap<String, Integer>();
		graph.edges().forEach(e -> {
			System.out.println(e.getAttribute("ui.color"));
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
				append(e + ": " + i + "\n", false, Color.blue);
			} catch (BadLocationException e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			} catch (IOException e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			}
		});
	}
	
	private void append (String text, boolean bold, Color c) throws BadLocationException, IOException {
		if(bold)
			text = "<b>"+text+"</b>";
		if(c != null)
			text = "<span style=\"color:"+c.toString()+";\">"+text+"</span>";
		kit.insertHTML(doc, doc.getLength(), text, 0, 0, null);
	}
	
	private void appendToPane(JTextPane tp, String msg, Color c, boolean bold) {
		StyleContext sc = StyleContext.getDefaultStyleContext();
		AttributeSet aset = sc.addAttribute(SimpleAttributeSet.EMPTY, StyleConstants.Foreground, c);

		if(!bold)
			aset = sc.addAttribute(aset, StyleConstants.FontFamily, "Lucida Console");
		else
			aset = sc.addAttribute(aset, StyleConstants.FontFamily, "Lucida Console Bold");

		aset = sc.addAttribute(aset, StyleConstants.Alignment, StyleConstants.ALIGN_JUSTIFIED);

		int len = tp.getDocument().getLength();
		tp.setCaretPosition(len);
		tp.setCharacterAttributes(aset, false);
		tp.replaceSelection(msg);
	}
}
