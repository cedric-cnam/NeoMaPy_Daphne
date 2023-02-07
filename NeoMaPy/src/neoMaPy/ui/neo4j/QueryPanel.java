/**
 * Created by Nicolas Travers <nicolas.travers@devinci.fr> 2022-2023©
 */
package neoMaPy.ui.neo4j;

import java.awt.BorderLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.IOException;

import javax.swing.JButton;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTextArea;
import javax.swing.ScrollPaneConstants;
import javax.swing.text.BadLocationException;

import neoMaPy.Query;
import neoMaPy.connection.Connection;

public class QueryPanel extends JPanel {
	/**
	 * 
	 */
	private static final long serialVersionUID = 5639974892840163200L;
	Query q;
	JTextArea text;
	JLabel status;
	NeoPanel np;

	QueryPanel(Query q, NeoPanel np) {
		super();
		this.np = np;
		setLayout(new BorderLayout());
		this.q = q;
		JButton b = new JButton("<html><b>" + q.instruction + "</b></html>");
		b.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				execute();
			}
		});
		add(b, BorderLayout.NORTH);

		text = new JTextArea(q.query);
		text.setLineWrap(true);
		text.setRows(6);
		add(new JScrollPane(text, ScrollPaneConstants.VERTICAL_SCROLLBAR_ALWAYS, ScrollPaneConstants.HORIZONTAL_SCROLLBAR_NEVER),
				BorderLayout.CENTER);
		add(status = new JLabel("    "), BorderLayout.SOUTH);
	}

	boolean execute() {
		String query = text.getText();
		try {
			if (q.instruction.compareTo("Load CSV") == 0) {
				String file = query.substring(query.indexOf("file:/") + 6);
				file = file.substring(0, file.indexOf("\""));
				try {
					Connection.updateQuery(query);

				} catch (Exception e) {
					JOptionPane.showMessageDialog(this, "The CSV file cannot found.\n\n\"" + file
							+ "\"\n\nPut it in the 'import' folder of your Neo4j project.");
					return false;
				}
			} else {
				String[] queries = query.split(";");
				for (String q : queries)
					try {
						Connection.updateQuery(q);
					} catch (Exception e) {
						JOptionPane.showMessageDialog(this,
								"Something wrong happened in query \"" + this.q.instruction + "\"\n" + e.getMessage());
						return false;
					}
			}
			status.setText("<html><b>done</b></html>");
			np.updateStats();
		} catch (BadLocationException | IOException e) {
			e.printStackTrace();
		}
		return true;
	}

	void setText() {
		text.setText(q.query);
	}
}
