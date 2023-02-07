/**
 * Created by Nicolas Travers <nicolas.travers@devinci.fr> 2022-2023©
 */
package neoMaPy.ui.graphstream.info;

import java.awt.BorderLayout;

import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JProgressBar;

public class MAPBar extends JPanel {
	/**
	 * 
	 */
	private static final long serialVersionUID = 4427580560264894678L;
	private JProgressBar pb;
	private JLabel l;
	private final int maxStatus = 10;

	public MAPBar() {
		super(new BorderLayout());
		add(l = new JLabel("MAP status"), BorderLayout.WEST);
		add(pb = new JProgressBar(0, maxStatus), BorderLayout.CENTER);

	}

	public void setLabel(String label) {
		System.out.println(label);
		l.setText("MAP status (" + label + ")");
	}

	public void setBarMax(int value) {
		pb.setMaximum(value);
	}

	public void resetStatus() {
		pb.setValue(0);
	}

	public void changeStatus() {
		pb.setValue(pb.getValue() + 1);
	}
}
