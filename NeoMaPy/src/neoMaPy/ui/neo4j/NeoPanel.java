/**
 * Created by Nicolas Travers <nicolas.travers@devinci.fr> 2022-2023©
 */
package neoMaPy.ui.neo4j;

import java.awt.BorderLayout;
import java.awt.GridLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import javax.swing.BoxLayout;
import javax.swing.JButton;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JPasswordField;
import javax.swing.JProgressBar;
import javax.swing.JScrollPane;
import javax.swing.JTextField;
import javax.swing.JTextPane;
import javax.swing.text.BadLocationException;
import javax.swing.text.html.HTMLDocument;
import javax.swing.text.html.HTMLEditorKit;

import neoMaPy.NeoMaPy;
import neoMaPy.Query;

public class NeoPanel extends JPanel implements ActionListener{
	/**
	 * 
	 */
	private static final long serialVersionUID = -1302983545774175051L;

	private JTextField uri, db, user, mdp;
	private JTextPane dbStats;
	private JLabel status;
	private JButton connect, exec;
	private JProgressBar pb;

	private HTMLEditorKit kit = new HTMLEditorKit();
    private HTMLDocument doc;
    private List<QueryPanel> queriesPanel = new ArrayList<QueryPanel> ();
    private List<Query> queries;

	public NeoPanel (int width, int height) {
		super();
		setSize(width, height);
		setLayout(new BorderLayout ());
		
		JPanel connection = new JPanel (new BorderLayout ());
		connection.add(new JLabel ("<html><b>Connection to Neo4j</b></html>"), BorderLayout.NORTH);
		JPanel connectionStrings = new JPanel (new GridLayout(2,5));
		connectionStrings.add(new JLabel("URI"));
		connectionStrings.add(new JLabel("Database"));
		connectionStrings.add(new JLabel("User"));
		connectionStrings.add(new JLabel("Password"));
		connectionStrings.add(connect = new JButton("Connection"));
		connectionStrings.add(uri = new JTextField((String) NeoMaPy.config.get("URI")));
		connectionStrings.add(db = new JTextField((String) NeoMaPy.config.get("database")));
		connectionStrings.add(user = new JTextField((String) NeoMaPy.config.get("user")));
		connectionStrings.add(mdp = new JPasswordField((String) NeoMaPy.config.get("mdp")));
			connect.addActionListener(this);
		connectionStrings.add(status = new JLabel ("<html><b><center>NOT CONNECTED</center></b></html>"));
		connection.add(connectionStrings, BorderLayout.CENTER);
		
		add(connection, BorderLayout.NORTH);
		
		this.setVisible(true);
	}

	private void db () {
		JPanel stats = new JPanel (new BorderLayout ());

		stats.add(new JLabel ("<html><b>Databases content</b></html>"), BorderLayout.NORTH);

		JPanel queriesP = new JPanel (new BorderLayout ());
		queriesP.add(new JScrollPane (queries((String) NeoMaPy.config.get("generateGraphQueries")),
	            JScrollPane.VERTICAL_SCROLLBAR_ALWAYS,
	            JScrollPane.HORIZONTAL_SCROLLBAR_NEVER), BorderLayout.CENTER);
		
		JPanel p = new JPanel(new GridLayout (1,2));		
		p.add(exec = new JButton("Execute all queries"));
		exec.addActionListener(new ActionListener () {
			@Override
			public void actionPerformed(ActionEvent e) {
				executeQueries ();
			}
			
		});
		p.add(pb = new JProgressBar(0, queriesPanel.size()));
		pb.setStringPainted(true);
		queriesP.add(p, BorderLayout.NORTH);
		
		dbStats = new JTextPane ();
		dbStats.setSize(200, 100);
		dbStats.setContentType("text/html");
		dbStats.setEditorKit(kit);
		dbStats.setEditable(false);
		try {
			updateStats ();
		} catch (BadLocationException | IOException e) {
			e.printStackTrace();
		}
		queriesP.add(dbStats, BorderLayout.EAST);

		stats.add(queriesP, BorderLayout.CENTER);

		add(stats, BorderLayout.CENTER);
	}

	@SuppressWarnings("unchecked")
	public void connect() {
		NeoMaPy.config.put("URI", uri.getText());
		NeoMaPy.config.put("database", db.getText());
		NeoMaPy.config.put("user", user.getText());
		NeoMaPy.config.put("mdp", mdp.getText());
		if(NeoMaPy.connection ()) {
			status.setText("<html><b><center>CONNECTED</center></b></html>");
			db ();
		} else
			status.setText("<html><b><center>NOT CONNECTED</center></b></html>");
	}

	public void executeQueries() {
		new Thread(new Runnable() {
            @Override 
            public void run() 
            {
            	pb.setValue(0);
            	for(QueryPanel qp : queriesPanel) {
        			if(!qp.execute())
        				return;
        			pb.setValue(pb.getValue()+1);
                    try
                    {
                        Thread.sleep(50);

                    }
                    catch(Exception e)
                    {
                        e.printStackTrace();
                    }
                }
            }   
        }).start();
	}
	
	private JPanel queries (String queriesFile) {
		if(queriesPanel.size() > 0)
			return null;
		queries = NeoMaPy.readQueries(queriesFile);
		JPanel p = new JPanel (new GridLayout(10, 1, 50, 50));
		p.setLayout(new BoxLayout(p, BoxLayout.PAGE_AXIS));
		QueryPanel previousPanel = null;
		for(Query q: queries) {
			if(previousPanel != null && q.instruction.compareTo(previousPanel.q.instruction) ==0) {
				previousPanel.q.query += "\n"+q.query;
				previousPanel.setText();
			} else {
				previousPanel = new QueryPanel (q, this);
				p.add(previousPanel);
				queriesPanel.add(previousPanel);
			}
		}
		return p;
	}

	public List<Query> getQueries (){
		return queries;
	}
	
	void updateStats () throws BadLocationException, IOException {
		Map<String, Integer> stats = NeoMaPy.statQueries();

		doc = new HTMLDocument ();
		dbStats.setDocument(doc);
		try {
			append("Number of Concepts\n", true, null);
		} catch (BadLocationException | IOException e) {
			e.printStackTrace();
		}
		append(stats.get("Concepts").toString(), false, null);
		append("\n\nNumber of TFs\n", true, null);
		append(stats.get("TFs").toString(), false, null);
		append("\n\nNumber of Conflicts\n", true, null);
		append(stats.get("Conflicts").toString(), false, null);
		append("\n\nNumber of Inferences\n", true, null);
		append(stats.get("Inferences").toString(), false, null);
	}

	private void append (String text, boolean bold, String c) throws BadLocationException, IOException {
		if(bold)
			text = "<b>"+text+"</b>";
		if(c != null)
			text = "<span style=\"color:"+c+";\">"+text+"</span>";
		kit.insertHTML(doc, doc.getLength(), text, 0, 0, null);
	}

	@Override
	public void actionPerformed(ActionEvent e) {
		if(e.getSource() == connect) {
			connect();
		}
	}
}
