/**
 * Created by Nicolas Travers <nicolas.travers@devinci.fr> 2022-2023©
 */
package neoMaPy.ui.graphstream;

import java.awt.BorderLayout;
import java.io.IOException;
import java.util.List;

import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTextPane;
import javax.swing.text.BadLocationException;
import javax.swing.text.html.HTMLDocument;
import javax.swing.text.html.HTMLEditorKit;

import neoMaPy.Query;
import neoMaPy.ui.graphstream.info.GraphInfoPanel;

public class ConflictInfoPanel extends JPanel {
	/**
	 * 
	 */
	private static final long serialVersionUID = 2800380442407155164L;
	private JTextPane conflictInfo;
	private HTMLEditorKit kit = new HTMLEditorKit();
	private HTMLDocument doc = new HTMLDocument();

	ConflictInfoPanel(NeoMaPyGraph graph, List<Query> queries, int width, int height) {
		setLayout(new BorderLayout());
		add(new JLabel("Conflicts colors"), BorderLayout.NORTH);
		add(new JScrollPane(conflictInfo = new JTextPane()), BorderLayout.CENTER);
		conflictInfo.setSize(200, height);
		conflictInfo.setContentType("text/html");
		conflictInfo.setEditorKit(kit);
		conflictInfo.setDocument(doc);
		try {
			setConflictInfo(queries);
		} catch (BadLocationException | IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	private void setConflictInfo(List<Query> queries) throws BadLocationException, IOException {
		append("<html>", false, null);
		for (Query q : queries) {
			if (q.instruction.startsWith("Conflict")) {
				String code = q.instruction.substring(q.instruction.indexOf("-") + 2);
				if (code.indexOf(" -") > -1)
					code = code.substring(0, code.indexOf(" -"));
				else
					code = "TC1";
				String name = q.instruction.substring(q.instruction.lastIndexOf("-") + 2);
				append("<b>" + code + "</b> - " + name, false, GraphInfoPanel.rc.getColor(code));
			}
		}
		append("</html>", false, null);
	}

	private void append(String text, boolean bold, String c) throws BadLocationException, IOException {
		if (bold)
			text = "<b>" + text + "</b>";
		if (c != null)
			text = "<span style=\"color:" + c + ";\">" + text + "</span>";
		kit.insertHTML(doc, doc.getLength(), text, 0, 0, null);
	}
}
