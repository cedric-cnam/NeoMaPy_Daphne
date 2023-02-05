/**
 * Created by Nicolas Travers <nicolas.travers@devinci.fr> 2022-2023©
 */
package neoMaPy.ui;

import java.awt.GridLayout;
import java.awt.LayoutManager;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.JButton;
import javax.swing.JPanel;

import neoMaPy.ui.graphstream.GraphStreamPanel;

public class ButtonPanel extends JPanel implements ActionListener {
	/**
	 * 
	 */
	private static final long serialVersionUID = -3030023292690004897L;
	private JButton CSSButton = new JButton("CSS reload");
	private JButton layout = new JButton("Stop Layout");
	private boolean layoutEnabled = true;
	private GraphStreamPanel gs;

	public ButtonPanel(GraphStreamPanel gs) {
		super();
		this.gs = gs;
		this.setLayout(new GridLayout(1, 2));
		this.add(CSSButton);
		this.add(layout);
		setButtons();
	}

	private void setButtons() {
		CSSButton.addActionListener(this);
		layout.addActionListener(this);
	}

	@Override
	public void actionPerformed(ActionEvent e) {
		if (e.getSource() == CSSButton) {
			gs.getGraph().css();
		} else if (e.getSource() == layout) {
			if (layoutEnabled)
				;//gs.viewer.disableAutoLayout();
			else
				;//gs.viewer.enableAutoLayout();
			layoutEnabled = !layoutEnabled;
		}

	}
}
